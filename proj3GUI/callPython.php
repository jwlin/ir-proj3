<?php

$command = escapeshellcmd('python test.py '.$_POST['inputValue']);
$output = shell_exec($command);
echo $output;

?>