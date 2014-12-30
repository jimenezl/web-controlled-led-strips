$(document).foundation();

initialSlidersUpdate();

//CHANGE THESE 5 COLORS FOR CUSTOM COLORS
var customColor1 = "1 1 1";
var customColor2 = "2 2 2";
var customColor3 = "3 3 3";
var customColor4 = "4 4 4";
var customColor5 = "5 5 5";

var sliderCount1 = 0;
var sliderCount2 = 0;
var sliderCount3 = 0;
var sliderCount4 = 0;
var sliderCount5 = 0;
var sliderCount6 = 0;

//For some reason, whenever the page is loaded, the slider change functions are called a number of times. 
//This is a workaround, since we don't want premature calls
var minSliderCount = 34;


$('#Slider1').on('change.fndtn.slider', function(){
sliderCount1++;
	console.log(sliderCount1);
	if ((sliderCount1 > minSliderCount) && (sliderCount1 % 3 == 0)){
		console.log("writing to text file: " + $('#Slider1').attr('data-slider'));
		writeColorData();
	}
});

$('#Slider2').on('change.fndtn.slider', function(){
sliderCount2++;
	console.log(sliderCount2);
	if ((sliderCount2 > minSliderCount) && (sliderCount2 % 3 == 0)){
		console.log("writing to text file: " + $('#Slider2').attr('data-slider'));
		writeColorData();
	}
});

$('#Slider3').on('change.fndtn.slider', function(){
sliderCount3++;
	console.log(sliderCount3);
	if ((sliderCount3 > minSliderCount) && (sliderCount3 % 3 == 0)){
		console.log("writing to text file: " + $('#Slider3').attr('data-slider'));
		writeColorData();
	}
});

$('#BrightnessSlider').on('change.fndtn.slider', function(){
sliderCount4++;
	console.log(sliderCount4);
	if ((sliderCount4 > minSliderCount) && (sliderCount4 % 3 == 0)){
		console.log("writing to text file: " + $('#BrightnessSlider').attr('data-slider'));
		writeBrightnessData();
	}
});

$('#FadeSpeedSlider').on('change.fndtn.slider', function(){
sliderCount5++;
	console.log(sliderCount5);
	if ((sliderCount5 > minSliderCount) && (sliderCount5 % 3 == 0)){
		console.log("writing to text file: " + $('#FadeSpeedSlider').attr('data-slider'));
		writeFadeSpeedData();
	}
});

$('#StrobeSpeedSlider').on('change.fndtn.slider', function(){
sliderCount6++;
	console.log(sliderCount6);
	if ((sliderCount6 > minSliderCount) && (sliderCount6 % 3 == 0)){
		console.log("writing to text file: " + $('#StrobeSpeedSlider').attr('data-slider'));
		writeStrobeSpeedData();
	}
});

//SETTING BUTTON CLICK FUNCTIONS

$("#fade1").click(function(){
	console.log("fade 1");
	writeCustomSetting(1);
});

$("#fade2").click(function(){
	console.log("fade 2");
	writeCustomSetting(2);
});

$("#fade3").click(function(){
	console.log("fade 3");
	writeCustomSetting(3);
});

$("#fade4").click(function(){
	console.log("fade 4");
	writeCustomSetting(4);
});

$("#fade5").click(function(){
	console.log("fade 5");
	writeCustomSetting(5);
});

// COLOR BUTTON CLICK FUNCTIONS

$("#color1").click(function(){
	console.log("color 1");
	writeCustomColor(customColor1);
});

$("#color2").click(function(){
	console.log("color 2");
	writeCustomColor(customColor2);
});

$("#color3").click(function(){
	console.log("color 3");
	writeCustomColor(customColor3);
});

$("#color4").click(function(){
	console.log("color 4");
	writeCustomColor(customColor4);
});

$("#color5").click(function(){
	console.log("color 5");
	writeCustomColor(customColor5);
});

$("#redButton").click(function(){
	console.log("red");
	writeCustomColor("100 0 0");
});

$("#greenButton").click(function(){
	console.log("green");
	writeCustomColor("0 100 0");
});

$("#blueButton").click(function(){
	console.log("blue");
	writeCustomColor("0 0 100");
});

$("#resetButton").click(function(){
	console.log("reset");
	writeToFile("sentReset", "sent");
});

$("#partyButton").click(function(){
	console.log("party");
	$('#BrightnessSlider').foundation('slider', 'set_value', 100);
$('#FadeSpeedSlider').foundation('slider', 'set_value', 75);
$('#StrobeSpeedSlider').foundation('slider', 'set_value', 50);
if($("#strobeSwitch").prop("checked")){
	//pass
} else {
	$("#strobeSwitch").prop("checked", true);
	toggleStrobe();
}

//^^don't know why I have to do that

writeFadeSpeedData();
writeBrightnessData();
writeStrobeSpeedData();

$(document).foundation();
$(document).foundation('slider', 'reflow');
//^^this doesn't work, but is necessary for vv to work :O
writeCustomSetting(5);
setTimeout(function(){window.location.reload();}, 2000);


});

$("#randomButton").click(function(){
	console.log("random - not implemented yet");
	//TODO: implement
});

//POWER AND STROBE BUTTONS

// $("#powerButton").click(function(){
//     		console.log("power");
//     		writeToFile("sentPower", "sent");
// });

function togglePower(){
console.log("power");
	writeToFile("sentPower", "sent");
}

// $("#strobeButton").click(function(){
//     		console.log("strobe");
//     		writeToFile("sentStrobeToggle", "sent");
// });

function toggleStrobe(){
console.log("strobe");
	writeToFile("sentStrobeToggle", "sent");
}


function writeToFile(key, stringToWrite)
{
	$.ajax({
            type: "POST",
            url: "receiving_file.php",
            data: key+ '=' + stringToWrite,
            success:function(data){
            }
    });

}

function writeColorData(){
writeToFile("sentColor", $('#Slider1').attr('data-slider') + " " + $('#Slider2').attr('data-slider') + " " + $('#Slider3').attr('data-slider'));
}

function writeBrightnessData(){
writeToFile("sentBrightness", $('#BrightnessSlider').attr('data-slider'));
}

function writeFadeSpeedData(){
writeToFile("sentSpeed", $('#FadeSpeedSlider').attr('data-slider'));
}

function writeStrobeSpeedData(){
writeToFile("sentStrobe", $('#StrobeSpeedSlider').attr('data-slider'));
}

function writeCustomColor(customColor){
writeToFile("sentColor", customColor);
setTimeout(function(){window.location.reload();}, 1000);
}

function writeCustomSetting(settingNumber){
writeToFile("sentSetting", settingNumber);
}

function initialSlidersUpdate() {
var response = $.ajax({ type: "GET",   
            url: "displayData.php",   
            async: false
          }).responseText;
var currentSliderData = response.split(" ");

$('#Slider1').foundation('slider', 'set_value', currentSliderData[1]);
$('#Slider2').foundation('slider', 'set_value', currentSliderData[2]);
$('#Slider3').foundation('slider', 'set_value', currentSliderData[3]);
$('#BrightnessSlider').foundation('slider', 'set_value', currentSliderData[7]);
$('#FadeSpeedSlider').foundation('slider', 'set_value', currentSliderData[9]);
$('#StrobeSpeedSlider').foundation('slider', 'set_value', currentSliderData[11]);

if (currentSliderData[12] == "on"){
	$("#strobeSwitch").prop("checked", true);
} else {
	$("#strobeSwitch").prop("checked", false);
}

if (currentSliderData[14] == "on"){
	$("#powerSwitch").prop("checked", true);
} else {
	$("#powerSwitch").prop("checked", false);
}

$(document).foundation();
$(document).foundation('slider', 'reflow');

}