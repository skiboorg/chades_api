from .self_Alipay import *
import qrcode,time

alipay = alipay()

class pay:
    def __init__(self,out_trade_no,total_amount,subject,timeout_express):
        self.out_trade_no = out_trade_no
        self.total_amount = total_amount
        self.subject = subject
        self.timeout_express = timeout_express

    def get_qr_code(self,code_url):
        '''
        生成二维码
        :return None
        '''
        qr = qrcode.QRCode(
             version=1,
             error_correction=qrcode.constants.ERROR_CORRECT_H,
             box_size=10,
             border=1
        )
        qr.add_data(code_url)  # 二维码所含信息
        img = qr.make_image()  # 生成二维码图片
        img.save(r'E:\python3\Alipay_for_QR_code\qrcode_image\qr_test_ali.png')
        print('二维码保存成功！')

    def query_order(self,out_trade_no: int):
        '''
        :param out_trade_no: 商户订单号
        :return: Nonem
        '''
        _time = 0
        for i in range(600):
            time.sleep(1)
            result = alipay.init_alipay_cfg().api_alipay_trade_query(out_trade_no=out_trade_no)
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                print('订单已支付!')
                print('订单查询返回值：', result)
                return True
            _time += 2
        return False


def do_payment():
    payer = pay(out_trade_no=datetime.now().strftime('%Y%m%d%H%M%S'),total_amount= 6,subject = "test",timeout_express='10m')

    dict = alipay.trade_pre_create(out_trade_no=payer.out_trade_no,total_amount=payer.total_amount,subject =payer.subject,timeout_express=payer.timeout_express )

    payer.get_qr_code(dict['qr_code'])
    payer.query_order(payer.out_trade_no)