import unittest2 as unittest
from mock import patch, Mock

from add_aws_roles import RoleAdder


class TestRoleAdder(unittest.TestCase):

    def setUp(self):
        self.roles = ['devfoo', 'devbar']
        self.prefix = 'rz_'
        self.trusted_arn = 'arn:test'

    @patch('add_aws_roles._boto_connect')
    def test_initialization_of_role_adder(self, boto_connect_mock):
        access_key_id = None
        secret_access_key = None
        role_adder = RoleAdder(
            self.roles,
            self.prefix,
            self.trusted_arn,
            access_key_id,
            secret_access_key,
        )
        self.assertEqual(self.roles, role_adder.roles)
        self.assertEqual(self.prefix, role_adder.prefix)
        self.assertEqual(self.trusted_arn, role_adder.trusted_arn)
        boto_connect_mock.assert_called_once_with(None, None)

    @patch('add_aws_roles._boto_connect')
    def test_initialization_of_role_adder_with_aws_credentials(self, boto_connect_mock):
        access_key_id = 'access_key_id'
        secret_access_key = 'secret_access_key'
        role_adder = RoleAdder(
            self.roles,
            self.prefix,
            self.trusted_arn,
            access_key_id,
            secret_access_key,
        )
        boto_connect_mock.assert_called_once_with('access_key_id', 'secret_access_key')


class TestAddingRoles(unittest.TestCase):

    @patch('add_aws_roles._boto_connect')
    def setUp(self, mock_boto_connect):
        self.mock_boto_connection = Mock()
        mock_boto_connect.return_value = self.mock_boto_connection
        self.roles = ['devfoo', 'devbar']
        self.prefix = 'rz_'
        self.trusted_arn = 'arn:test'
        access_key_id = None
        secret_access_key = None
        self.role_adder = RoleAdder(
            self.roles,
            self.prefix,
            self.trusted_arn,
            access_key_id,
            secret_access_key,
        )

    def test_add_role_should_call(self):
        self.role_adder.add_role('devfoo')
        self.mock_boto_connection.create_role.assert_called_once_with('devfoo')