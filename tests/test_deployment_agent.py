import pytest
import yaml
from unittest.mock import patch, MagicMock
from src.deployment_agent import DeploymentAgent
import tempfile
import os

@pytest.fixture
def config_file():
    config = {
        'environments': {
            'test': {
                'url': 'http://test.example.com',
                'health_check_path': '/health',
                'deploy_timeout': 300,
                'retry_interval': 1,
                'max_retries': 2
            }
        },
        'deployment_steps': [
            {
                'name': 'backup',
                'type': 'command',
                'command': 'echo "backup"'
            },
            {
                'name': 'install_dependencies',
                'type': 'command',
                'command': 'echo "installing"'
            }
        ],
        'rollback_steps': [
            {
                'name': 'restore',
                'type': 'command',
                'command': 'echo "restoring"'
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        yaml.dump(config, f)
        temp_path = f.name
    
    yield temp_path
    os.unlink(temp_path)

@pytest.fixture
def agent(config_file):
    agent = DeploymentAgent(config_file)
    agent.set_environment('test')
    return agent

def test_load_config(agent):
    assert 'environments' in agent.config
    assert 'test' in agent.config['environments']
    assert agent.config['environments']['test']['url'] == 'http://test.example.com'

def test_set_environment(agent):
    assert agent.current_env == 'test'
    with pytest.raises(ValueError):
        agent.set_environment('nonexistent')

@patch('subprocess.run')
def test_run_command_success(mock_run, agent):
    mock_run.return_value = MagicMock(returncode=0)
    assert agent._run_command('echo "test"') is True
    mock_run.assert_called_once()

@patch('subprocess.run')
def test_run_command_failure(mock_run, agent):
    mock_run.side_effect = subprocess.CalledProcessError(1, 'failed command')
    assert agent._run_command('invalid command') is False

@patch('requests.get')
def test_health_check_success(mock_get, agent):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'status': 'ok'}
    mock_get.return_value = mock_response
    
    assert agent._check_health() is True
    assert mock_get.call_count == 1

@patch('requests.get')
def test_health_check_failure(mock_get, agent):
    mock_get.side_effect = requests.RequestException
    assert agent._check_health() is False
    assert mock_get.call_count == 2  # max_retries = 2

@patch('subprocess.run')
def test_deploy_success(mock_run, agent):
    mock_run.return_value = MagicMock(returncode=0)
    assert agent.deploy() is True
    assert mock_run.call_count == 2  # two command steps

@patch('subprocess.run')
def test_deploy_failure_with_rollback(mock_run, agent):
    mock_run.side_effect = [
        MagicMock(returncode=0),  # backup succeeds
        subprocess.CalledProcessError(1, 'failed command')  # install fails
    ]
    assert agent.deploy() is False
    assert agent.backup_created is True
    # Check that rollback was attempted
    assert mock_run.call_count == 3  # backup + failed install + rollback 