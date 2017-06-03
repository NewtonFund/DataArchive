<?php

  //$MNTTZ = new DateTimeZone('America/Denver');

  $username = "hidden_from_github!";
  $password = "hidden_from_github!";
  $server   = "hidden_from_github!";
  $database = "hidden_from_github!";

  $db = new mysqli($server,$username,$password,$database);

  if($db->connect_errno > 0){
    die('Unable to connect to database [' . $db->connect_error . ']');
  }

  // Construct a query
  $feed_id = $_GET["feed"];
  $feed_name = "feed_".$feed_id ;
  $start = $_GET["start"]/1000;
  $end = $_GET["end"]/1000;

  $sql = "SELECT time*1000 as time,data FROM ".$feed_name." WHERE time > ".$start." AND time < ".$end ; 
  if(!$result = $db->query($sql)){
    die('There was an error running the query [' . $db->error . ']');
  }

  $json = array();

  $num_rows = $result->num_rows;
  
  // Extract a max of 1000 rows from the $result
  //$step = ceil($num_rows / 1000);
  // Extract all
  $step = 1;
  
  if ( $step > 1 ) {
    for ($ii=0; $ii<$num_rows; $ii+=$step) {
      // This looks like it ought to be horribly inefficient. Need to re-think this code.
      $result->data_seek($ii);
      array_push($json, $result->fetch_row() );
    }
  } else {
    for ($ii=0; $ii<$num_rows; $ii++) {
      array_push($json, $result->fetch_row() );
    }
  }

  echo json_encode($json, JSON_NUMERIC_CHECK);

  $result->free();

  $db->close();

?>
