<html>
    <head>
        <title>ACP brevet REST-API</title>
    </head>

    <body>
        <h1>List of Times</h1>
        <ul>
            <?php
            $data = file_get_contents('http://acpbrevets-service'.$_SERVER['REQUEST_URI']);
            $obj = json_decode($data);
            if(isset($_SERVER['REDIRECT_URL'])){
                $url = "".$_SERVER['REDIRECT_URL'];
                $type = preg_split('~/~', $url);
            }
            else{
                $type = preg_split('~/~', "/");
            }
            
            if(strcmp(end($type), "csv") !== 0){ // if it doesn't end with csv then its json format.
                $brevetList = $obj->brevets;
                foreach ($brevetList as $brevet) {
                    echo "<h2>Distance: $brevet->distance</h2>";
                    echo "<h2>Begin Date: $brevet->begin_date</h2>";
                    echo "<h2>Begin Time: $brevet->begin_time</h2>";
                    $controlnum = 0;
                    foreach ($brevet->controls as $control) {
                        echo "<br>Control: $controlnum </br>"; // = I'd like 5 waffles
                        echo "<li>km: $control->km</li>";
                        echo "<li>miles: $control->miles</li>";
                        echo "<li>location: $control->location</li>";
                        if(isset($control->open)){
                            echo "<li>open time: $control->open</li>";
                        }
                        if(isset($control->close)){
                            echo "<li>close time: $control->close</li>";
                        }
                        $controlnum++;
                        echo "---------------------------------";
                    }
                    echo "--------------------------------------";
                }
            }
            else{
                $csv = str_getcsv($data, "\n");
                if(empty($data) == 0){
                    echo "<table>";
                    foreach($csv as &$Row){
                        $entry = str_getcsv($Row, ",");
                        foreach($entry as &$item){
                                echo "<td> <input  readonly='true' value=$item> </td>";   
                        }
                        echo "</tr>";
                    }
                    echo "</table>";
                }
            }
            ?>
        </ul>
    </body>
</html>
