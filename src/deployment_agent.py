import yaml
import time
import subprocess
import requests
import logging
from typing import Dict, List, Any
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeploymentAgent:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
        self.current_env = None
        self.backup_created = False

    def _load_config(self) -> Dict:
        """Load deployment configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def set_environment(self, env: str):
        """Set the target environment for deployment."""
        if env not in self.config['environments']:
            raise ValueError(f"Environment {env} not found in config")
        self.current_env = env
        logger.info(f"Set deployment environment to: {env}")

    def _run_command(self, command: str) -> bool:
        """Execute a shell command and return success status."""
        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e}")
            return False

    def _check_health(self) -> bool:
        """Check if the application is healthy."""
        env_config = self.config['environments'][self.current_env]
        url = f"{env_config['url']}{env_config['health_check_path']}"
        max_retries = env_config['max_retries']
        retry_interval = env_config['retry_interval']

        for attempt in range(max_retries):
            try:
                response = requests.get(url)
                if response.status_code == 200 and response.json()['status'] == 'ok':
                    logger.info("Health check passed")
                    return True
                logger.warning(f"Health check failed, attempt {attempt + 1}/{max_retries}")
            except requests.RequestException as e:
                logger.warning(f"Health check request failed: {e}")
            
            if attempt < max_retries - 1:
                time.sleep(retry_interval)

        return False

    def _execute_step(self, step: Dict[str, Any]) -> bool:
        """Execute a deployment step based on its type."""
        step_type = step['type']
        logger.info(f"Executing step: {step['name']}")

        if step_type == 'command':
            return self._run_command(step['command'])
        elif step_type == 'service':
            return self._run_command(step['command'])
        elif step_type == 'http':
            return self._check_health()
        else:
            logger.error(f"Unknown step type: {step_type}")
            return False

    def deploy(self) -> bool:
        """Execute the deployment process."""
        if not self.current_env:
            raise ValueError("Environment not set")

        logger.info(f"Starting deployment to {self.current_env}")
        
        # Execute deployment steps
        for step in self.config['deployment_steps']:
            if not self._execute_step(step):
                logger.error(f"Deployment failed at step: {step['name']}")
                self.rollback()
                return False
            
            if step['name'] == 'backup':
                self.backup_created = True

        logger.info("Deployment completed successfully")
        return True

    def rollback(self) -> bool:
        """Execute rollback steps if deployment fails."""
        if not self.backup_created:
            logger.warning("No backup found, cannot rollback")
            return False

        logger.info("Starting rollback process")
        
        for step in self.config['rollback_steps']:
            if not self._execute_step(step):
                logger.error(f"Rollback failed at step: {step['name']}")
                return False

        logger.info("Rollback completed successfully")
        return True

if __name__ == '__main__':
    # Example usage
    agent = DeploymentAgent('deployment_config.yaml')
    agent.set_environment('development')
    success = agent.deploy()
    logger.info(f"Deployment {'succeeded' if success else 'failed'}") 