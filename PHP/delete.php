<?php
$filename = $_GET['file'];

if (file_exists($filename)) {
    if (!strpos($filename,'.php')){
        if (unlink($filename)) {
    echo "True";
  //删除成功
}
else {
    echo "False";
  //删除失败
}
}

else {
    echo "非法操作";
}
    }

    else{
        echo "Null";
          //文件不存在
    }


?>
