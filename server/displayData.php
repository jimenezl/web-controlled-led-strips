<?php
    $myfilename = "data.txt";
    if(file_exists($myfilename)){
      echo file_get_contents($myfilename);
    }
?>