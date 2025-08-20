# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-

{
    "name": "Test report - BG111 Thai Form",
    "version": "18.0.1.0.0",
    "author": "Ecosoft",
    "category": "Training",
    "license": "AGPL-3",
    "depends": ["hr_expense"],
    "data": [
        "data/paperformat_data.xml",      # ✅ โหลดก่อน
        "reports/expenses_form.xml",      # ✅ โหลดทีหลัง
    ],
    "assets": {
        'web.report_assets_common': [
            'day/static/scss/style_report.scss',
        ],
    },
    "external_dependencies": {
        "python": ['num2words'],  # ✅ สำหรับแปลงตัวเลขเป็นคำ (ถ้าต้องการ)
    },
    "installable": True,
    "auto_install": False,
    
}