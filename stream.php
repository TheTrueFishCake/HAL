<?php
set_time_limit(0);
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');

$log="activity.log";
$viewers="viewers.txt";

if(!file_exists($viewers)) file_put_contents($viewers,"0");

function update($d){
    global $viewers;
    $c=(int)file_get_contents($viewers);
    $c+=$d;
    if($c<0)$c=0;
    file_put_contents($viewers,$c);
}

update(1);
register_shutdown_function(function(){update(-1);});

$last=0;

while(true){

    echo "event: viewers\n";
    echo "data: ".file_get_contents($viewers)."\n\n";

    if(file_exists($log)){
        $size=filesize($log);
        if($size>$last){
            $f=fopen($log,"r");
            fseek($f,$last);
            $data=fread($f,$size-$last);
            fclose($f);

            $last=$size;

            echo "event: log\n";
            echo "data: ".str_replace("\n","\\n",$data)."\n\n";
        }
    }

    ob_flush();
    flush();
    usleep(500000);
}
