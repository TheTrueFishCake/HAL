<?php
$env="env";
$zip=tempnam(sys_get_temp_dir(),"hal").".zip";

$z=new ZipArchive();
$z->open($zip,ZipArchive::CREATE);

$files=new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($env)
);

foreach($files as $file){
    if(!$file->isDir()){
        $z->addFile($file->getRealPath(),
        substr($file->getRealPath(),strlen($env)+1));
    }
}

$z->close();

header("Content-Type: application/zip");
header("Content-Disposition: attachment; filename=hal_env.zip");
readfile($zip);
unlink($zip);
