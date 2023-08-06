from unittest import TestCase
import threading
import time

from pymicroservice.client.remote_service import RemoteService
from pymicroservice import PyMicroService, public_method, private_api_method
from pymicroservice.errors import CalledServiceError

HOST, PORT = "127.0.0.1", 6799
PORT2 = PORT + 1


class Service1(PyMicroService):
    name = "test.service.client.1"

    host = HOST
    port = PORT

    @public_method
    def method1(self):
        return "hello there"

    @public_method
    def method2(self, arg):
        return "hello there {}".format(arg)

    @public_method
    def method3(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Bad type for a and b")
        return a + b

    @public_method
    def method4(self, arg1, arg2):
        return {"arg1": arg1, "arg2": arg2}

    @private_api_method
    def method5(self, name):
        return "private {}".format(name)

    def api_token_is_valid(self, api_token):
        return api_token == "test-token"


class Service2(PyMicroService):
    name = "test.service.client.2"
    api_token_header = "Custom-Header"
    host = HOST
    port = PORT2

    @private_api_method
    def test(self):
        return True

    def api_token_is_valid(self, api_token):
        return api_token == "test-token"


class ClientTestCase(TestCase):
    service_thread = None
    service_thread2 = None
    service_url = "http://127.0.0.1:6799/api"
    service_url2 = "http://127.0.0.1:6800/api"

    @classmethod
    def setUpClass(cls):
        service1 = Service1()
        service2 = Service2(io_loop=service1.io_loop)
        cls.service_thread = threading.Thread(target=service1.start, daemon=True)
        cls.service_thread.start()

        cls.service_thread2 = threading.Thread(target=service2.start, daemon=True)
        cls.service_thread2.start()

        time.sleep(1)  # wait for the servers to be ready to accept connections

    def test_client_connection(self):
        client = RemoteService(self.service_url)

        self.assertEqual(client.name, "test.service.client.1")
        self.assertCountEqual(client.get_available_methods(),
                              ["get_service_specs", "method1", "method2", "method3", "method4", "method5"])

    def test_method_call_no_args(self):
        client = RemoteService(self.service_url)

        result = client.methods.method1()
        self.assertEqual(result, "hello there")

    def test_method_call_with_args(self):
        client = RemoteService(self.service_url)

        result = client.methods.method2("hello")
        self.assertEqual(result, "hello there hello")

    def test_method_call_with_numeric_args(self):
        client = RemoteService(self.service_url)
        result = client.methods.method3(10, 11)
        self.assertEqual(result, 21)

        result = client.methods.method3(1, 1)
        self.assertEqual(result, 2)

        result = client.methods.method3(131, 33)
        self.assertEqual(result, 164)

        with self.assertRaisesRegex(CalledServiceError, "Bad type for a and b"):
            result = client.methods.method3("abc", "def")

    def test_method_call_with_complex_result(self):
        client = RemoteService(self.service_url)
        result = client.methods.method4(arg1="test", arg2="success")
        self.assertEqual(result, {"arg1": "test", "arg2": "success"})

        result = client.methods.method4("test", "success")
        self.assertEqual(result, {"arg1": "test", "arg2": "success"})

    def test_method_call_method_does_not_exist(self):
        client = RemoteService(self.service_url)
        with self.assertRaises(AttributeError):
            result = client.methods.does_not_exist()

    def test_method_call_wrong_params(self):
        client = RemoteService(self.service_url)
        with self.assertRaises(CalledServiceError):
            result = client.methods.method1(param="should_not_be_here")

        with self.assertRaises(CalledServiceError):
            result = client.methods.method1(1, 2, 3)

    def test_method_call_private_token_missing(self):
        client = RemoteService(self.service_url)  # no api token
        with self.assertRaises(CalledServiceError):
            result = client.methods.method5("test")

    def test_method_call_private_token_ok(self):
        client = RemoteService(self.service_url, api_key="test-token")
        result = client.methods.method5("test")
        self.assertEqual(result, "private test")

    def test_method_call_private_token_incorrect(self):
        client = RemoteService(self.service_url, api_key="wrong-token")
        with self.assertRaises(CalledServiceError):
            result = client.methods.method5("test")

    def test_method_call_custom_api_token_header(self):
        client = RemoteService(self.service_url2, api_header="Custom-Header", api_key="test-token")
        result = client.methods.test()
        self.assertTrue(result)

    def test_notifications(self):
        client = RemoteService(self.service_url)
        response = client.notifications.method1()
        self.assertIsNone(response)

    def test_notifications_method_not_found(self):
        client = RemoteService(self.service_url)
        with self.assertRaises(AttributeError):
            response = client.notifications.does_not_exist()

    def test_notifications_bad_params(self):
        client = RemoteService(self.service_url)
        response = client.notifications.method1(1, 2, 3)
        self.assertTrue(response is None)  # every notification should return None because
                                           # do not care about the answer


if __name__ == '__main__':
    Service1().start()
