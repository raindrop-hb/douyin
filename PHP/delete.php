<?php
$filename = $_GET['file'];

if (file_exists($filename)) {
    if (!strpos($filename,'.php')){
        if (unlink($filename)) {
    echo "True";
  //ɾ���ɹ�
}
else {
    echo "False";
  //ɾ��ʧ��
}
}

else {
    echo "�Ƿ�����";
}
    }

    else{
        echo "Null";
          //�ļ�������
    }


?>
