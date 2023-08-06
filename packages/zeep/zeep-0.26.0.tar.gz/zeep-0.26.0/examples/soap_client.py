import zeep


def run_tests():
    transport = zeep.Transport(cache=None)
    client = zeep.Client('http://localhost:8000/?wsdl', transport=transport)

    res = client.service.echo_bytearray(b'\x00\x01\x02\x03\x04')
    print(res)


if __name__ == '__main__':
    run_tests()
