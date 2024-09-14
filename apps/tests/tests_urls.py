from rest_framework.reverse import reverse_lazy


class TestUrl:
    def test_auth(self):
        url = reverse_lazy('send_code')
        assert url == '/api/v1/auth/send-code/'
        url = reverse_lazy('verify_code')
        assert url == '/api/v1/auth/verify/'
