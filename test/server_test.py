

# class TestServer:
#     def test_start_a_server(self, database, cleanup_database):
#         httpserver = HTTPServer(port=3333)
#         httpserver.start()
#         httpserver.expect_request("/test").respond_with_data("helloworld")
#         print("----------------->", httpserver.url_for("/test"))

#         assert 1 == 1
#         time.sleep(240)
