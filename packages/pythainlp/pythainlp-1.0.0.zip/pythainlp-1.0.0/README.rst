PyThaiNLP
=========

[|PyPI Downloads|][|pypi|](https://pypi.python.org/pypi/pythainlp)
|Build Status|

Thai NLP in python package.

Natural language processing หรือ การประมวลภาษาธรรมชาติ โมดูล PyThaiNLP
เป็นโมดูลที่ถูกพัฒนาขึ้นเพื่องานวิจัยและพัฒนาการประมวลภาษาธรรมชาติภาษาไทยในภาษา
Python

รองรับทั้ง Python 2.7 และ Python 3

-  เอกสารการใช้งาน : https://pythonhosted.org/pythainlp/
-  หน้าหลัก GitHub : https://github.com/wannaphongcom/pythainlp

สถานะโครงการ
~~~~~~~~~~~~

กำลังพัฒนา

Version
~~~~~~~

1.0.0

ความสามารถ
~~~~~~~~~~

-  ตัดคำภาษาไทย
-  ถอดเสียงภาษาไทยเป็น Latin
-  Postaggers ภาษาไทย
-  อ่านตัวเลขเป็นข้อความภาษาไทย
-  เรียงจำนวนคำของประโยค
-  แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา
-  เช็คคำผิดในภาษาไทย
-  และอื่น ๆ

ติดตั้ง
=======

รองรับทั้ง Python 2.7 และ Python 3

รุ่นเสถียร

.. code:: sh

    $ pip3 install pythainlp

รุ่นกำลังพัฒนา

.. code:: sh

    $ git clone https://github.com/wannaphongcom/pythainlp.git
    $ cd pythainlp
    $ python setup.py install

เอกสารการใช้งานเบื้องต้น
========================

ตัวอย่างการใช้งาน

.. code:: python

    # ตัดคำ
    from pythainlp.segment import segment
    a = 'ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'
    b = segment(a)
    print(b) # ['ฉัน', 'รัก', 'ภาษาไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คนไทย']
    # Postaggers ภาษาไทย
    from pythainlp.postaggers import tag
    print(tag('คุณกำลังประชุม')) # [('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')]
    # หาคำที่มีจำนวนการใช้งานมากที่สุด
    from pythainlp.rank import rank
    aa = rank(b)
    print(aa) # Counter({'ฉัน': 2, 'ไทย': 2, 'เป็น': 1, 'รัก': 1, 'ภาษา': 1, 'เพราะ': 1, 'คน': 1})
    # ถอดเสียงภาษาไทยเป็น Latin
    from pythainlp.romanization import romanization
    b=romanization("แมว")
    print(b) # mæw
    # แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา
    from pythainlp.change import *
    a="l;ylfu8iy["
    a=texttothai(a)
    b="นามรสนอำันี"
    b=texttoeng(b)
    print(a) # สวัสดีครับ
    print(b) # ok,iloveyou
    # เปลี่ยนตัวเลขเป็นตัวอักษรภาษาไทย (เงินบาท)
    from pythainlp.number import numtowords
    print("5611116.50")
    print(numtowords(5611116.50)) # ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์

License
~~~~~~~

Apache Software License 2.0

พัฒนาโดย นาย วรรณพงษ์ ภัททิยไพบูลย์

สนับสนุน
~~~~~~~~

คุณสามารถร่วมพัฒนาโครงการนี้ได้ โดยการ Fork และส่ง pull requests กลับมา

.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/pythainlp.png
.. |pypi| image:: https://img.shields.io/pypi/v/pythainlp.svg
.. |Build Status| image:: https://travis-ci.org/wannaphongcom/pythainlp.svg?branch=develop
   :target: https://travis-ci.org/wannaphongcom/pythainlp
