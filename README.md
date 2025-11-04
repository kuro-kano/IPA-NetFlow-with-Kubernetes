# 06016423 INFRASTRUCTURE PROGRAMMABILITY AND AUTOMATION (1/2025)

## ข้อมูลสถานศึกษา
**สถานศึกษา:** สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง  
**คณะ:** เทคโนโลยีสารสนเทศ  
**สาขา:** เทคโนโลยีสารสนเทศ  
**แขนง:** โครงสร้างพื้นฐานเทคโนโลยีสารสนเทศ

## ข้อมูลสมาชิก
- นายไตรสิทธิ์ เจริญปริพัฒน์ 66070069
- นายธันยา วรมงคล 66070091
- นายพิสิษฐ์ งามเลิศพัฒนสิริ 66070136

## ภาพรวม
Project นี้คือระบบ Network Traffic Monitoring โดยใช้ NetFlow บน Kubernetes Cluster
ระบบนี้ประกอบด้วย Worker, RabbitMQ, MongoDB, และ Web ซึ่งทำงานร่วมกันเพื่อเก็บและแสดงผลข้อมูลการไหลของทราฟฟิก 
ภายในเครือข่ายจากอุปกรณ์ Cisco IOSv Router

## ความแตกต่างจาก Project ใน Class
- จากเดิมที่ให้ etcd กับ Control Plane อยู่ใน Nodes เดียวกัน แยกออกเป็น 2 Nodes
- เปลี่ยนจากใช้ ArgoCD เป็น FluxCD
- มีการติดตั้ง Velero เพื่อใช้ในการ backup ข้อมูลทั้งหมดของ etcd
- เปลี่ยนจากการใช้ worker ให้ใช้คำสั่ง show ip interface brief บน CiscoIOSv เป็นการตรวจสอบดู traffic โดยใช้ NetFlow v5

## วิธีการทำ
https://www.notion.so/IPA-NetFlow-with-Kubernetes-282c39426848807e857aefd5f145490f?source=copy_link

## คลิป Presentation
https://youtu.be/e-9-mHrtR4M?si=PSH8Ytg-H747aBnr

## หมายเหตุ
- ควรทำการ Fork ตัวของ Repository นี้แล้ว clone ไปใช้เป็นของตนเอง
- ใช้ในการทำ FluxCD
