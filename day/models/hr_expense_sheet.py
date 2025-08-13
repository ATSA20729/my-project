from odoo import models, fields, api
from odoo.tools import float_utils
import logging

_logger = logging.getLogger(__name__)

class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    
    # เพิ่มฟิลด์ที่อาจจะต้องการสำหรับ บก.111
    bg111_certification_text = fields.Text(
        string='ข้อความรับรong',
        default='ขอรับรองว่ารายจ่ายข้างต้นนี้ ไม่อาจเรียกใบเสร็จรับเงินจากผู้รับได้ และข้าพเจ้าได้จ่ายไปในงานของราชการโดยแท้'
    )
    
    signature_date = fields.Date(
        string='วันที่ลงชื่อ',
        default=fields.Date.context_today
    )
    
    @api.model
    def amount_to_text_thai(self, amount):
        """
        แปลงจำนวนเงินเป็นตัวอักษรภาษาไทย
        """
        if not amount:
            return "ศูนย์บาทถ้วน"
            
        try:
            # แยกส่วนจำนวนเต็มและทศนิยม
            amount_int = int(amount)
            amount_decimal = int(round((amount - amount_int) * 100))
            
            # ตัวเลขภาษาไทย
            thai_digits = ['ศูนย์', 'หนึ่ง', 'สอง', 'สาม', 'สี่', 'ห้า', 'หก', 'เจ็ด', 'แปด', 'เก้า']
            thai_units = ['', 'สิบ', 'ร้อย', 'พัน', 'หมื่ง', 'แสน', 'ล้าน']
            
            def convert_group(num):
                """แปลงเลขหลัก 1-6 หลัก"""
                if num == 0:
                    return ''
                
                result = ''
                digits = str(num)[::-1]  # กลับลำดับ
                
                for i, digit in enumerate(digits):
                    digit_int = int(digit)
                    if digit_int == 0:
                        continue
                        
                    if i == 0:  # หลักหน่วย
                        result = thai_digits[digit_int] + result
                    elif i == 1:  # หลักสิบ
                        if digit_int == 1:
                            if len(digits) == 1 or (len(digits) > 1 and int(digits[0]) == 0):
                                result = 'สิบ' + result
                            else:
                                result = 'สิบ' + result
                        elif digit_int == 2:
                            result = 'ยี่สิบ' + result
                        else:
                            result = thai_digits[digit_int] + 'สิบ' + result
                    else:  # หลักร้อย, พัน, หมื่น, แสน
                        if i < len(thai_units):
                            result = thai_digits[digit_int] + thai_units[i] + result
                
                return result
            
            # แปลงส่วนจำนวนเต็ม
            if amount_int == 0:
                text_baht = 'ศูนย์บาท'
            else:
                # แยกกลุ่มล้าน
                millions = amount_int // 1000000
                remainder = amount_int % 1000000
                
                text_baht = ''
                if millions > 0:
                    text_baht += convert_group(millions) + 'ล้าน'
                
                if remainder > 0:
                    text_baht += convert_group(remainder)
                
                text_baht += 'บาท'
            
            # แปลงส่วนสตางค์
            if amount_decimal == 0:
                text_satang = 'ถ้วน'
            else:
                text_satang = convert_group(amount_decimal) + 'สตางค์'
            
            return text_baht + text_satang
            
        except Exception as e:
            _logger.error(f"Error converting amount to Thai text: {e}")
            return f"{amount:,.2f} บาท"
    
    @api.model 
    def get_thai_date(self, date_obj):
        """
        แปลงวันที่เป็นรูปแบบไทย พ.ศ.
        """
        if not date_obj:
            return ''
            
        thai_months = [
            'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 
            'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 
            'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
        ]
        
        day = date_obj.day
        month = thai_months[date_obj.month - 1]
        year = date_obj.year + 543
        
        return f"{day} {month} {year}"
    
    @api.model
    def get_thai_weekday(self, date_obj):
        """
        แปลงวันในสัปดาห์เป็นภาษาไทย
        """
        if not date_obj:
            return ''
            
        thai_weekdays = [
            'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 
            'ศุกร์', 'เสาร์', 'อาทิตย์'
        ]
        
        return thai_weekdays[date_obj.weekday()]