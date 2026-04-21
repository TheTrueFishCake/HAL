<?php
$views_file = "views.txt";
if (!file_exists($views_file)) file_put_contents($views_file, "0");
$views = (int)file_get_contents($views_file) + 1;
file_put_contents($views_file, $views);
?>

<h1>HAL Terminal</h1>

<p>
Live Viewers: <span id="viewerCount">0</span> |
Total Views: <?php echo $views; ?>
</p>

<pre id="log"></pre>

<script>
const logEl = document.getElementById("log");
const viewerEl = document.getElementById("viewerCount");

const evtSource = new EventSource("stream.php");

evtSource.addEventListener("log", e => {
    let text = e.data.replace(/\\n/g,"\n");
    text.split("\n").forEach(line=>{
        let d=document.createElement("div");

        if(line.includes("THOUGHT")) d.style.color="cyan";
        else if(line.includes("ACTION")) d.style.color="red";
        else if(line.includes("RESULT")) d.style.color="yellow";
        else d.style.color="lime";

        d.textContent=line;
        logEl.appendChild(d);
    });
    logEl.scrollTop = logEl.scrollHeight;
});

evtSource.addEventListener("viewers", e=>{
    viewerEl.textContent = e.data;
});
</script>

<form action="download.php">
<button>Download HAL Environment</button>
</form>
