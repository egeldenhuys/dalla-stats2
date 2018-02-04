<?php
    //external file for all php functions used
    include_once 'phpFunctions.php';
    session_start();

    $conn = connect();

    if(isset($_SESSION["logedIn"]))
    {
      if(isset($_POST["name"]))
      {
        $name = $_POST["name"];
        $transfer = $_POST["transfer"];
        $friend = $_POST["friend"];

        echo $name . " " .$transfer ." ". $friend;

        $sql = "SELECT on_peak FROM users WHERE ID = '$name' OR ID = '$friend'";
        $result = $conn->query($sql);
        if ($result)
        {
            //first variable is the friends amount of bytes
            $row = $result->fetch_row();
            $friendsUsage =  $row[0];
            //second variableis your bytes
            $row = $result->fetch_row();
            $userUsage =  $row[0];

            $transfer = calculateBytes($transfer);

            // echo "<br />".round($friendsUsage,2).'<br />'.round($userUsage,2);

            $userUsage += $transfer;
            $friendsUsage -= $transfer;

            // echo "<br />".round($friendsUsage,2).'<br />'.round($userUsage,2);

            $sql = "UPDATE users SET on_peak = '$userUsage' WHERE ID = '$name'";
            if ($conn->query($sql) === TRUE)
            {

            }
            else
            {
                echo "Error: " . $sql . "<br>" . $conn->error;
            }
            $sql = "UPDATE users SET on_peak = '$friendsUsage' WHERE ID = '$friend'";
            if ($conn->query($sql) === TRUE)
            {

            }
            else
            {
                echo "Error: " . $sql . "<br>" . $conn->error;
            }

            header("Location: home.php?success='true'");
        }
        else
        {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
      }
    }
    else
    {
      header("Location: home.php");
    }

?>
