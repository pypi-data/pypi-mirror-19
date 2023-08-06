from stacktask_tempest_plugin.tests import base
from tempest import test
from tempest.lib.common.utils import data_utils


class StacktaskAdminTestUsers(base.BaseStacktaskTest):
    credential_roles = ['admin']

    @classmethod
    def resource_setup(cls):
        super(StacktaskAdminTestUsers, cls).resource_setup()

    @classmethod
    def resource_cleanup(cls):
        super(StacktaskAdminTestUsers, cls).resource_cleanup()

    @test.idempotent_id('8c3f736e-e071-11e5-9bf6-74d4358b0331')
    @test.services('identity')
    def test_invite_user(self):
        u_name = data_utils.rand_name('stacktask')
        u_email = '%s@example.com' % u_name
        u_password = data_utils.rand_password()
        u_roles = ['_member_']

        # invite the new user to tenant
        self.stacktask_client.user_invite(
            u_email,
            u_email,
            u_roles)

        # list users, confirm that the invited user appears.
        invited_user = self.get_user_by_name(u_email)
        self.assertEqual(invited_user['cohort'], 'Invited')
        self.assertEqual(invited_user['status'], 'Invited')

        # using the invited users id, bypass email and get the auth token
        # NOTE(dalees): Requires full 'admin' role to access sensitive tokens.
        token_id = self.get_token_by_taskid(invited_user['id'])
        self.stacktask_client.token_submit(
            token_id,
            {"password": u_password}
        )

        # Confirm user has been created in keystone
        ks_user = self.get_user_by_name(u_email, client='keystone')
        self.addCleanup(self.users_client.delete_user, ks_user['id'])
        st_user = self.get_user_by_name(u_email)
        self.assertEqual(st_user['cohort'], 'Member')
        self.assertEqual(st_user['status'], 'Active')
        self.assertEqual(st_user['id'], ks_user['id'])

        # Verify member role with keystone
        self.assert_user_roles(
            self.get_creds_project_id(), ks_user['id'], u_roles)
