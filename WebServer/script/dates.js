//DESCRIPTION: function used to predict your average of how many gigs you may use in the month

function daysInMonth(month, year) {

  var totalDays = new Date (year,month, 0).getDate();
  var currentDays = new Date().getDate();

  // console.log(currentDays + " " + totalDays);

  var gigs = document.getElementById("total").innerHTML;

  //the total gigs displayed is still a string
  // console.log(gigs);
  totalDays = parseFloat(totalDays);
  currentDays = parseFloat(currentDays);
  var usedGigs = parseFloat(gigs);
  var average = 0;
  var daysLeft = totalDays - currentDays;

  //after we parseFloat we can perform operations on usedGigs
  // console.log(usedGigs - 100);

  usedGigs /= currentDays;
  average = usedGigs;

  // console.log(usedGigs);
  // console.log(daysLeft + " Days left");

  usedGigs *= daysLeft;
  usedGigs = 120;
  // console.log(usedGigs);

  if(usedGigs > 450)
  {
    //very bad
    document.getElementById('average').innerHTML = "We are averaging " + average + "gs a day. We will use "+ usedGigs +"gs by the end of the month. SLOW DOWN!!"
    document.getElementById('average').style.color = "#f00";
  }
  else if(usedGigs > 350)
  {
    //average
    document.getElementById('average').innerHTML = "We are averaging " + average + "gs a day. We will use "+ usedGigs +"gs by the end of the month."
    document.getElementById('average').style.color = "#000";
  }
  else
  {
    //very good
    document.getElementById('average').innerHTML = "We are averaging " + average + "gs a day. We will use "+ usedGigs +"gs by the end of the month. Very good"
    document.getElementById('average').style.color = "#00f";
  }
}

   function person(month, year, user)
  {
    var name = user;
    var totalDays = new Date (year,month, 0).getDate();
    var currentDays = new Date().getDate();

    // console.log(currentDays + " " + totalDays);

    var userGigs = document.getElementById("onPeakUser").innerHTML;
    console.log(userGigs);

    //the total gigs displayed is still a string
    // console.log(gigs);
    totalDays = parseFloat(totalDays);
    currentDays = parseFloat(currentDays);
    var usedGigs = parseFloat(userGigs);
    var daysLeft = totalDays - currentDays;
    var average = 0;
    var days = 0;
    var total = 0;
    total = usedGigs;

    usedGigs /= currentDays;
    average = usedGigs;


    console.log(total);

    while (total <= 40 && days < 100)
    {
      days++;
      total += average;
    }

    if(days < daysLeft)
    {
      //will go over peak
      document.getElementById('daysTillPeak').innerHTML = user +" will reach 40gs in "+ days + " days. There are " + daysLeft + " days left this month!!!"
      document.getElementById('daysTillPeak').style.color = "#f00";
    }
    else
    {
      //will not go over peak
      document.getElementById('daysTillPeak').innerHTML = user +" will reach 40gs in "+ days + " days.  There are " + daysLeft + " days left this month"
      document.getElementById('daysTillPeak').style.color = "#00f";
    }


}
