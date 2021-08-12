//jenkins scripted pipeline

def BuildJob(projectName, stageName, params) {
    try {
        stage(stageName.toString()) {
            def e2e = build job:projectName, parameters: params, propagate: false
            result = e2e.result
            if (result.equals("SUCCESS")) { return (e2e.getDescription()) } 
            else { error e2e.getDescription() }
        }
    } catch (e) {
        currentBuild.result = "FAIL"
        result = "FAIL" 
    }
}

node ('common') {
    currentBuild.description = 'Temperature: ' + params.SP
    if (params.SN_IP.isEmpty()){ error('Some test variables are missing. Check Pipeline parameters.') }
    list_of_sn_ip = "${params.SN_IP}".split(',')

    //set the chamber temperature
    BuildJob('./step0_preset_chamber_temp', "Set temperature to ${params.SP} in the chamber", [string(name:'SP', value: params.SP)])
    sleep(1800)

    //pretest
    tests_to_run = [:]
    for (p in list_of_sn_ip) {
        def pair_sn_ip = p.split('-')
        def serial_num = pair_sn_ip[0]
        def uut_ip = pair_sn_ip[1]
        def test_params = [string(name: 'SERIAL_NUM', value: serial_num), string(name: 'UUT_IP', value: uut_ip)]
        tests_to_run["step1_preset_device_${serial_num}"] = {
            BuildJob('./step1_preset_device', "Preset device " + serial_num, test_params)
        }
    }
    parallel tests_to_run 
    sleep(30)

    //Power off
    BuildJob('./step2_power_off', "Turn off power ${params.AGILENT_IP}", [string(name:'AGILENT_PORT', value: params.AGILENT_PORT), 
    string(name:'AGILENT_IP', value: params.AGILENT_IP)])

    //battery_drain_detection
    tests_to_run = [:]
    for (p in list_of_sn_ip) {
        def pair_sn_ip = p.split('-')
        def serial_num = pair_sn_ip[0]
        def uut_ip = pair_sn_ip[1]
        def test_params = [string(name: 'SERIAL_NUM', value: serial_num), string(name: 'UUT_IP', value: uut_ip)]
        tests_to_run["step3_drain_battery_${serial_num}"] = {
            BuildJob('./step3_drain_battery', "Battery drain on device " + serial_num, test_params)
        }
    }
    parallel tests_to_run 
    //sleep(10)

    //Power on
    BuildJob('./step4_power_on', "Turn on power ${params.AGILENT_IP}", [string(name:'AGILENT_PORT', value: params.AGILENT_PORT), 
    string(name:'AGILENT_IP', value: params.AGILENT_IP)])

    //detection charging
    tests_to_run = [:]
    for (p in list_of_sn_ip) {
        def pair_sn_ip = p.split('-')
        def serial_num = pair_sn_ip[0]
        def uut_ip = pair_sn_ip[1]
        def test_params = [string(name: 'SERIAL_NUM', value: serial_num), string(name: 'UUT_IP', value: uut_ip)]
        tests_to_run["/step5_charging_battery_${serial_num}"] = {
            BuildJob('./step5_charging_battery', "detection batttery charging on device " + serial_num, test_params)
        }
    }
    parallel tests_to_run 
    sleep(30)

    //turn off the temp chamber
    BuildJob('./step6_turn_off_temp_chamber', "Turn off the temperature chamber", [])
}
