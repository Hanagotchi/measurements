from fastapi import status


class CalculatorController:
    def __init__(self, service):
        self.service = service

    def handle_sum(self, request):
        sum = request.number1 + request.number2
        self.service.add_number(sum)
        return {
            'result': sum,
            'status': status.HTTP_200_OK
        }
