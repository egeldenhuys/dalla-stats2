<?php
    //external file for all php functions used
    include_once 'phpFunctions.php';
    session_start();

    $conn = connect();

    if(isset($_SESSION["logedIn"]))
    {
      if($_SESSION["logedIn"] == $_GET["name"])
      {
        header("Location: home.php");
      }
    }

    if(isset($_POST["password2"]))
    {
      setUp($conn);
    }
    else if(isset($_POST["password"]))
    {
      loginUser($conn);
    }

    if(isset($_GET["name"]))
     {
         $name = $_GET["name"];
         if(!validName($conn, $name))
         {
            header("Location: index.php");
         }
         else
         {
           //start of the session
           $_SESSION["name"] = "$name";
           // echo $_SESSION["name"];
         }
         //check to see if the user has set a password or not
         if(!checkPassword($conn, $name))
         {
           SetPassword($conn, $name);
         }
         else
         {
            logIn($conn, $name);
         }
     }
     else if(isset($_SESSION["name"])) {
       //password was not correct usually end up here
       $name = $_SESSION["name"];

       if(!checkPassword($conn, $name))
       {
         SetPassword($conn, $name);
       }
       else
       {
          logIn($conn, $name);
       }
     }
     else {
       echo "Something went wrong aborting!";
     }


?>

<!DOCTYPE html>
<html>
  <meta charset="UTF-8">
  <meta name="description" content="Dalla stats">
  <meta name="keywords" content="HTML,CSS,XML,JavaScript">
  <meta name="author" content="Paul Wood">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="./bootstrap-3.3.4-dist/css/bootstrap.min.css">
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <script src="script/jquery-2.1.3.min.js"></script>
  <script type="text/javascript" src="script/animations.js"></script>
  <script src="script/dates.js"></script>
<body>

  <a href="index.php" id="home"><button type="button" class="btn btn-default">
    <span class="glyphicon glyphicon-home"></span>
  </button></a>

  <div class="row" id = "memebers">
  <?php
    $user = $_SESSION["name"];

    $sql = "SELECT on_peak, off_peak FROM person WHERE username = '$user'";
    $result = $conn->query($sql);

    if($result->num_rows > 0)
    {
      while($row = $result->fetch_assoc())
      {
        $gigsOn = calculateGigs($row["on_peak"]);
        $gigsOff = calculateGigs($row["off_peak"]);

        echo '<div class="col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1 col-xs-12" id="text">
             <div id="person_info">'.$user.'</div> <div id="onPeakUser">'.round($gigsOn, 2).'gs on Peak</div>
             <div id="offPeakUser">'.round($gigsOff, 2).'gs off Peak</div>
             </div>';
      }
    }

  ?>
</div>
     <div id="daysTillPeak"></div>
  <script>
      var month = new Date();
      var n = month.getMonth();
      n++;
      var user = "<?php echo "$user" ?>";

      person(n, 2018, user);
  </script>


</body>
</html>
