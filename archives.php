<?php
$dir="archives";
$files=array_filter(scandir($dir),fn($f)=>str_ends_with($f,".zip"));
rsort($files);
?>

<h1>HAL Archives</h1>

<?php foreach($files as $f): ?>
<div><a href="archives/<?php echo $f;?>"><?php echo $f;?></a></div>
<?php endforeach; ?>
