$.ajax({
    type: "POST",
    url: "http://localhost/genes",
    data: {genes: 'hello'},
    success: function(){
        console.log("success")
    },
    dataType: "JSON"
});
