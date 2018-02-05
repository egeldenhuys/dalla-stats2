<?php
    //external file for all php functions used
    include_once 'phpFunctions.php';
    $conn = connect();
    session_start();

    if(!isset($_SESSION["logedIn"]))
    {
      header("Location: index.php");
    }
    if(isset($_POST["friend"]))
    {
      checkUsage($conn);
    }
    checkSuccess();

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
  <a href="logout.php" id="logout"><button type="button" class="btn btn-default">
    <span>Logout</span>
  </button></a>

  <h2>Signed in as <?php echo $_SESSION["logedIn"]; ?></h2>
  <h1>Send Data To</h1>

    <div class="row">
      <div class="col-md-12">
        <form action="home.php" method="post" id="form">
          <select name="friend" class="form-control" id="dropDown">
            <?php

            $user = $_SESSION["logedIn"];

            $sql = "SELECT username FROM person WHERE username != '$user'";
            $result = $conn->query($sql);

            if($result->num_rows > 0)
            {
              while($row = $result->fetch_assoc())
              {
                  echo '<option value="'.$row["ID"].'">'.$row["ID"].'</option>';
              }
            }
             ?>
          </select>
          <br><br>
          <div class="form-group">
            <label class="control-label col-sm-2" for="amt">Amount:</label>
            <div class="col-sm-10">
              <select class="form-control" id="amt" name="amt">
                <script>
                  for(var x = 1; x <= 30; x++)
                  {
                    document.write('<option value = '+x+'>'+x+'</option>')
                  }
                </script>
              </select>
            </div>
          </div>
          <br><br>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-block btn-info" id="confirmSubmit">Submit</button>
            </div>
          </div>
          </form>
      </div>
    </div>

    <div id="confirmPosition"></div>
    <div id="sendData"></div>


</body>
</html>
