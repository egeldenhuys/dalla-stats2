<?php
    //external file
    include_once 'phpFunctions.php';
    $conn = connect();
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

  <div class="row">
    <div class="col-md-12">
        <h1>Total Usage on Peak</h1>
        <div id="total_gigs"></div>
    </div>
  </div>


  <div class="row" id = "memebers">
    <?php
      //get username, on peak and off peak usage
      $result = selectData($conn);

      //total + totalOff are used to store the accumulated total of everyones usage this month
      $total = 0;
      $totalOff = 0;

      if($result->num_rows > 0)
      {
        //output each row one by one
        while($row = $result->fetch_assoc())
        {
          //convert bytes to gigs as each value read from the databse is stored in bytes
          $gigsOn = calculateGigs($row["on_peak"]);
          $gigsOff = calculateGigs($row["off_peak"]);


          //nice little php trick to close the php tag and code back in html prevents one giant echo
          ?>
           <div class="col-md-3 col-md-offset-0 col-sm-4 col-sm-offset-1 col-xs-12" id="text">
             <!-- DESCRIPTION: id="name"
                each name is read from the database and displayed as a link
                a href="user.php"?name = ''; this link allows us to send the users name clicked on to users.php
                by sending the name across we can collect data such as whos page we are logging in to and that users data

                again we switch from html to php when we want to access php variables
              -->
              <div id="name">
                  <a href="user.php?name=<?php echo $row["ID"]; ?>"><?php echo $row["ID"]; ?></a>
              </div>
              <!-- DESCRIPTION: id="name"
                 The order in which users appear is determined by this variable (ORDER BY was done in selectData())
                 round to 2 decimal places
               -->
              <div id="onPeak">
                <?php  echo round($gigsOn, 2); ?>gs on Peak
              </div>
              <div id="offPeak">
                <?php  echo round($gigsOff, 2); ?>gs off Peak
              </div>
          </div>


          <?php
          //reopen the php tag where you want to continue

          $total += $gigsOn;
          $totalOff += $gigsOff;
        }

      }

    ?>

  </div>
  <div id='heading'>
    <?php
      echo "<span id='total'>". round($total,2) . "</span><sub>gs</sub>";
    ?>
    <div id="average"></div>
  </div>
  <div id='footer'>
    <?php
      echo "<span id='totalOff'>". round($totalOff,2) . "</span><sub>gs</sub> Have been used in off Peak hours";
    ?>
    <div id="average"></div>
  </div>


<!-- the script that calculates how many days there are left in the month and our average for the month so far  -->
  <script>
      var month = new Date();
      var n = month.getMonth();
      n++;

      daysInMonth(n, 2018);
  </script>


</body>
</html>
