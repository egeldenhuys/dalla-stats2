<?php

//DESCRIPTION: connect to the database return the connection variable
function connect()
{
  $servername = "db";
  $username = "dalla";
  $password = "example";
  $db = "dalla_stats";

  $conn = new mysqli($servername, $username, $password, $db);

  if($conn->connect_error)
  {
    die("connection to database failed: " . $conn->connect_error);
  }

  return $conn;
}

//FUNCTION NAME: selectData
//DESCRIPTION: reads data from the users table and orders it according to on_peak desc
function selectData($conn)
{
  $sql = "SELECT username, on_peak, off_peak FROM person ORDER BY on_peak DESC";
  $result = $conn->query($sql);

  //Test the link if result returns true a successfull call to the databse was made and the result should be returned
  if ($result)
  {
    //returns to index.php
    return $result;
  }
  else
  {
      echo "Error: " . $sql . "<br>" . $conn->error;
  }
}

//DESCRIPTION: getGigs from bytes
function calculateGigs($bytes)
{
  //1 gb = 1073741824 bytes
  return $bytes / 1073741824;
}
//DESCRIPTION: getBytes from bytes
function calculateBytes($gigs)
{
  //1 gb = 1073741824 bytes
  return $gigs * 1073741824;
}

//DESCRIPTION: checks the databse to see if a valid name has been selected
function validName($conn, $name)
{
  $sql = "SELECT username FROM person";
  $result = $conn->query($sql);

  if($result->num_rows > 0)
  {
    while($row = $result->fetch_assoc())
    {
      if($row["username"] == $name)
      {
        return true;
      }
    }
  }
  return false;
}


//DESCRIPTION: checks the database and logs users into there home page if valid password
function validatePassword($conn, $user, $psw)
{
  $sql = "SELECT password FROM person WHERE username = '$user'";
  $result = $conn->query($sql);
  $row = $result->fetch_assoc();

  //echo $row['password'];

  if($row['password'] == $psw)
  {
      return true;
  }
}
//
function checkPassword($conn, $user)
{
  $sql = "SELECT password FROM person WHERE username = '$user'";
  $result = $conn->query($sql);
  $row = $result->fetch_assoc();

  if($row['password'] == null)
  {
      return false;
  }
  return true;
}

//function to display the form used to login. Is shown once the password has been set up for the user
function login($conn, $name)
{
  echo '<div class="row">
    <div class="col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1 col-xs-12">
      <h1>Sign in as '.$name.'</h1>
      <form class="form-horizontal" action="user.php" method="post">
        <div class="form-group">
          <label class="control-label col-sm-2" for="pwd">Password:</label>
          <div class="col-sm-10">
            <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="password">
            <input type="hidden" name="name" id="hiddenField" value="'.$name.'" />
          </div>
        </div>
        <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
          <button type="submit" class="btn btn-block btn-info">Submit</button>
        </div>
      </div>
      </form>
    </div>
  </div>';
}
//function to display the form used to set up the user password
function SetPassword($conn, $name)
{
  echo '<div class="row">
    <div class="col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1 col-xs-12">
      <h1>A password has not been set up for '.$name.'</h1>
      <form class="form-horizontal" action="user.php" method="post">
        <div class="form-group">
          <label class="control-label col-sm-2" for="pwd">Password:</label>
          <div class="col-sm-10">
            <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="password" />
            <input type="hidden" name="name" id="hiddenField" value="'.$name.'" />
          </div>
        </div>
        <div class="form-group">
          <label class="control-label col-sm-2" for="pwd2">Re-enter:</label>
          <div class="col-sm-10">
              <input type="password" class="form-control" id="pwd2" placeholder="Re-enter password" name="password2">
          </div>
        </div>
        <div class="form-group">
          <label class="control-label col-sm-2" for="key">Key:</label>
          <div class="col-sm-10">
              <input type="password" class="form-control" id="key" placeholder="Enter Your Key" name="key">
          </div>
        </div>
        <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
          <button type="submit" class="btn btn-block btn-info">Submit</button>
        </div>
      </div>
      </form>
    </div>
  </div>';
}

function setUp($conn)
{
  $password = $_POST["password"];
  $password2 = $_POST["password2"];
  $key = $_POST["key"];
  $user = $_SESSION["name"];

  if($password != $password2)
  {
      ?>
        <div class="alert alert-danger alert-dismissable fade in">
        <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
        <strong>Passwords do not match!</strong> Make sure your passwords are the same
        </div>
      <?php
  }
  else
  {
    $sql = "SELECT otp FROM person WHERE username = '$user'";
    $result = $conn->query($sql);
    $row = $result->fetch_assoc();

    if($row['otp'] != $key)
    {
      ?>
        <div class="alert alert-danger alert-dismissable fade in">
        <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
        <strong>Your Key was incorrect</strong>
        </div>
      <?php
    }
    else
    {
      $sql = "UPDATE person SET password = '$password' WHERE username = '$user'";
      if ($conn->query($sql) === TRUE)
      {
        ?>
           <div class="alert alert-success alert-dismissable fade in">
           <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
           <strong>Successfully added your password to the database</strong>
           </div>
        <?php
      }
      else
      {
          echo "Error: " . $sql . "<br>" . $conn->error;
      }

    }
  }

}
function loginUser($conn)
{
  $user = $_POST["name"];
  $valid = validatePassword($conn, $user, $_POST["password"]);

  if(!$valid)
  {
    ?>
      <div class="alert alert-danger alert-dismissable fade in">
      <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
      <strong>Password is incorrect</strong>
      </div>
    <?php
  }
  else
  {
    $_SESSION["logedIn"] = $_POST['name'];
    echo $_SESSION["logedIn"];
    header("Location: home.php");
  }
}

function checkUsage($conn)
{
    $user = $_SESSION['logedIn'];
    $transfer = $_POST['amt'];
    $friend = $_POST['friend'];

    $sql = "SELECT on_peak FROM person WHERE username = '$user'";
    $result = $conn->query($sql);
    $row = $result->fetch_assoc();

    $used = $row['on_peak'];

    $used = calculateGigs($used);

    if($used + $transfer > 40)
    {
      ?>
        <div id="confirm">
          <div class="alert alert-danger alert-dismissable fade in">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            <strong>You are not capable of sending <?php echo $transfer; ?>gs!</strong> Select a smaller amount
          </div>
      </div>
      <?php
    }
    else
    {
      ?>
        <div id="confirm">
          <div class="alert alert-danger alert-dismissable fade in">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            <strong id="passed">Confirm You want to send <?php echo $transfer; ?>gs to <?php echo $friend; ?></strong>

            <form action="transfer.php" method="post" id="form">
                <button type="submit" class="btn btn-block btn-primary">Submit</button>
                <input type="hidden" name="name" value="<?php echo $user; ?>" />
                <input type="hidden" name="transfer" value="<?php echo $transfer; ?>" />
                <input type="hidden" name="friend" value="<?php echo $friend; ?>" />
            </form>

          </div>


        </div>
      <?php
    }


}
function checkSuccess()
{
    if(isset($_GET["success"]))
    {
      ?>
        <div class="alert alert-success alert-dismissable fade in" id="confirm">
          <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
        <strong>Successfully sent data</strong>
        </div>
      <?php
    }
}

?>
