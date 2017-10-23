var dataArray = [];
 var checkedCheckboxes = [];
 function drawGraph() {
   var firstUser = dataArray.slice(-2)[0];
   var secondUser = dataArray.slice(-1)[0];
   var chart = new CanvasJS.Chart('chartContainer', {
       theme: "theme2",
       title: {
         text: 'Members Comparison, Height and Calories '
       },
       animationEnabled: true,
       legend: {
         cursor: 'pointer',
         itemclick: function (e) {
           if (typeof (e.dataSeries.visible) === 'undefined' || e.dataSeries.visible) {
             e.dataSeries.visible = false;
           } else {
             e.dataSeries.visible = true;
           }
           chart.render();
         }
       },
       axisY: {
         title: 'Metrics'
       },
       data: [
         {
           type: 'column',
           showInLegend: true,
           name: firstUser.username,
           dataPoints: [
             { y: firstUser.height, label: 'Height' },
             { y: firstUser.calories, label: 'Calories x10' }
           ]
         },
         {
           type: 'column',
           showInLegend: true,
           name: secondUser.username,
           dataPoints: [
             { y: secondUser.height, label: 'Height' },
             { y: secondUser.calories, label: 'Calories x10' }
           ]
         }
       ]
     });
   chart.render();
 }
 $(document).on('change', '#member_row', function () {
   var row = $(this).closest('#member_row');
   var cbox = row.find('#current_selected_member');
   var atLeastTwoChecked = $('#current_selected_member:checked').length > 1;
   var uncheckAuser = $('#current_selected_member:checked').length > 2;
   var username = row.find('td').eq(1).text();
   var data;
   var userId;
   var userData;
   var udata;
   var firstCheck;
   var item;
   checkedCheckboxes.push(cbox);

   if ($(cbox).prop('checked') === false) {
     for (item in dataArray) {
       if (Object.prototype.hasOwnProperty.call(dataArray, item)) {
         data = dataArray[item];
         if (data.username === username) {
           dataArray.pop(item);
           break;
         }
       }
     }
   } else {
     data = $('#member_row').data('memberdata');
     userId = row.find('td:first').text();
     userId = parseInt(userId, 10);
     userData = data[userId];
     udata = { username: username,
       calories: userData.calories,
       height: userData.height, };
     dataArray.push(udata);
   }
   if (atLeastTwoChecked) {
     $('.compare_button').removeClass('disabled');
     $('#msg').hide();
     $('#chartContainer').show();
     drawGraph();
   } else {
     $('.compare_button').addClass('disabled');
     $('#msg').show();
     $('#chartContainer').hide();
   }
   if (uncheckAuser) {
     firstCheck = checkedCheckboxes[0];
     firstCheck.attr('checked', false);
     checkedCheckboxes.splice(checkedCheckboxes.indexOf(firstCheck), 1);
   }
 });
