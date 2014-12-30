<?php
    $colors = $_POST['sentColor'];
    $brightness = $_POST['sentBrightness'];
    $setting = $_POST['sentSetting'];
    $speed = $_POST['sentSpeed'];
    $strobe = $_POST['sentStrobe'];
    $strobeToggle = $_POST['sentStrobeToggle'];
    $togglePower = $_POST['sentPower'];
    $reset = $_POST['sentReset'];

    $currentFileData = trim(file_get_contents('data.txt'));

    $splitLine = explode(" ", $currentFileData);

    if (!empty($togglePower)){
    	if ($splitLine[14] === "on"){
    		$splitLine[14] = "off";
    	}
    	else {
    		$splitLine[14] = "on";
    	}
    } 

    if (!empty($colors)){
    	$explodedColors = explode(" ", $colors);
		$splitLine[1] = $explodedColors[0];
		$splitLine[2] = $explodedColors[1];
		$splitLine[3] = $explodedColors[2];

		$splitLine[5] = 0;
    }

    if (!empty($setting)){
		$splitLine[5] = $setting;
    }

    if (!empty($brightness)){
		$splitLine[7] = $brightness;
    }

    if (!empty($speed)){
		$splitLine[9] = $speed;
    }

    if (!empty($strobe)){
		$splitLine[11] = $strobe;
    }

    if (!empty($strobeToggle)){
    	if ($splitLine[12] === "on"){
    		$splitLine[12] = "off";
    	}
    	else {
    		$splitLine[12] = "on";
    	}
		
    }

    file_put_contents('data.txt', implode(" ", $splitLine));

    if (!empty($reset)){
		file_put_contents('data.txt', file_get_contents('defaultData.txt'));
    }
    
    ?>