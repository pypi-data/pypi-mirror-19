# mobagel-python-sdk

## Introduce

MoBagel is a real-time cloud analytics platform that helps IoT companies monitor and analyze hardware usage, speed up research and development, forecast sales and marketing strategies, and proactively engage with customers to prevent product returns. As a result, companies can also save up to millions in cost reductions.

## Installation
Before run mobagel-python-sdk, you need to install [pip](https://pip.pypa.io/en/stable/) first.
### pip (Mac OS X)
```shell
	$ sudo easy_install pip
```
### pip (Ubuntu 14.04)
```shell
	$ sudo apt-get install python-pip python-dev build-essential 
	$ sudo pip install --upgrade pip 
```
### mobagel-python-sdk
```shell
	$ sudo pip install mobagel-python-sdk
```

## Getting Started

#### - Creating an account

If you do not have an account, please create an account [here](https://app.mobagel.com/signup). After you create an account, you will be directed to the dashboard.

#### - Creating a new product
To use MoBagel, you first have to create a product, which is essentially a group of same device. You will be prompted to create a new product when you first enter the dashboard.

After you create a product, you can go to Configuration -> Device Info to retrieve your product_key, which will be used to create device later on.

#### - Adding custom properties
In the Configuration, you can add custom properties to your product. Custom properties should have the following requirements:

* **ID**: Property ID (with the exception of state) should always begin with c_ to indicate that it is a custom property. In addition, property IDs are unique and cannot repeat with itself.

* **Name**: The property name is your nickname for your property. For example, if your ID is 'c_012421', you can set the name as 'temperature'. The modules in the dashboard will display your property name instead of your property ID.

* **Type**: There are two types of properties: category and numeric. Category uses a set of string options and numeric uses numeric options (optional).

* **Options**:
    - **Category**: please add all the possible string values of your property by typing in the options column. The server will use this to prevent your devices from sending erroraneous reports.
    
    - **Numeric** (optional): please set a min and max value for your numeric property to help protect your data from errors. For example, if your numeric property is humidity level, then you can set min and max to 0 and 100, respectively. This will allow our system to reject any reports with humidity levels that are not in this range because those values are theoretically impossible (i.e. negative humidity level).

Please note that you must configure your properties in your configuration before you send your first customized report.

#### - Register your first device
Once you generated a product_key from the dashboard, you can use the product_key and registerDevice function to register a device in your application.

	# Import package
	import pybagel
	import json

	product_key = "YOUR_PRODUCT_KEY"
	# Initialize a Client Instance by product_key
	client = pybagel.Client(product_key=product_key)
	
	# Register a device_key by client
	code, content = client.registerDevice()
	response = json.loads(content.decode('utf-8'))
	device_key = response["data"]["attributes"]["key"];
	# Save device_key


#### - Connecting custom properties or events
In your device application, you will need to prepare your report before sending it to MoBagel.

* Determining different states of your devices to send along with your report

		# Example states

		"state": "normal"
		"state": "error"

* Adding custom properties or events with a key beginning with c_

		# Example custom properties or events

		"c_temperature": 30
		"c_event": "turned_on"
* Deciding when to send reports (time, frequency, events)


#### - Sending first report
Once you connect the sensor properties, you can generate a report with the sendReport function.

    # Sample report
	device_key = "YOUR_DEVICE_KEY"
	report_content = {
	            "state": "Put your state here!",
	            "c_customization" : "python_sdk_test",
	            "c_develop_zone" : "PythonSDK"
	        }
	
	# SendReport
	code, content = client.sendReport(
	    device_key=device_key,
	    content=report_content
	)
	client.sendReport(device_key, content)

## Full sample
You can see example codes at github: /mobagel-python-sdk/example/
[click me](https://github.com/MoBagel/mobagel-python-sdk/tree/master/example)


	__author__ = "MoBagel Inc."
	
	import json
	import pybagel
	from pprint import pprint
	
	print "\nThis is MoBagel Python SDK sample, you can learn how to `register device` and `report state` in this sample code\n"
	
	product_key = "1111111111222222222233333333334444444444555555555566666666667777"
	# Initialize a Client Instance by product_key
	client = pybagel.Client(product_key=product_key)
	
	print "Register device..."
	# register a device_key by client
	code, content = client.registerDevice()
	response = json.loads(content.decode('utf-8'))
	print "Data response: "
	pprint(response)
	
	print "\n========================================================\n"
	
	print "Send report..."
	
	device_key = response["data"]["attributes"]["key"];
	content = {
	            "state": "Put your state here!",
	            "c_customization" : "python_sdk_test",
	            "c_develop_zone" : "PythonSDK"
	        }
	
	# SendReport
	code, content = client.sendReport(
	    device_key=device_key,
	    content=content
	    )
	# return report_id and report_timestamp
	response = json.loads(content.decode('utf-8'))
	print "Data response: "
	pprint(response)




## More
You can visit our home page and get more information.
[https://mobagel.com](https://mobagel.com)

## Author

MoBagel, us@mobagel.com

## License

MoBagel Software Development Kit (SDK) License Agreement


Subject to the terms of this License Agreement, you are hereby granted a worldwide, royalty-free, non-assignable, non-exclusive, and non-sublicensable license to use, copy, modify, and distribute this software in source code or binary form to use the SDK solely to develop applications to connect with MoBagel’s platform.

MoBagel owns all legal right, title and interest in and to the SDK. MoBagel reserves all rights not expressly granted to you. 

The form and nature of the SDK that MoBagel provides may change without prior notice to you. This SDK is provided “as is”, without warranty of any kind, express or limited. MoBagel may stop (permanently or temporarily) providing the SDK to users at MoBagel's sole discretion without prior notice.

You are not granted the right to use MoBagel’s trademarks, logos, domain names, or other distinctive brand features. 
