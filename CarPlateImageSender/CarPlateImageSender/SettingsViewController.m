//
//  SettingsViewController.m
//  CarPlateImageSender
//
//  Created by User on 12/9/12.
//  Copyright (c) 2012 Voronezh State University. All rights reserved.
//

#import <stdint.h>

#import "SettingsViewController.h"
#import "Globals.h"

@interface SettingsViewController ()

@end

@implementation SettingsViewController
@synthesize ipTextField = _ipTextField;
@synthesize portTextField = _portTextField;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
	if (!self)
		return self;
	
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];

	_ipTextField.keyboardType = UIKeyboardTypeDecimalPad;

	NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
	NSString *ip = [defaults objectForKey:userDefaultsIpAddressKey];
	if (ip)
	{
		_ipTextField.text = ip;
	}

	uint16_t port = [((NSNumber *)[defaults objectForKey:userDefaultsPortNumberKey]) unsignedIntValue];
	if (port)
	{
		_portTextField.text = [NSString stringWithFormat:@"%d", (int)port];
	}

}

- (void)viewDidUnload
{
	self.ipTextField = nil;
	self.portTextField = nil;
    [super viewDidUnload];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void)dealloc {
	[_ipTextField release];
	[_portTextField release];
	[super dealloc];
}



- (IBAction)saveButtonTriggered:(id)sender
{
	NSString *ipString = _ipTextField.text;
	NSString *portString = _portTextField.text;


	// Validate IP address
	NSString *ipRegex = @"\\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b";
	NSPredicate *ipPredicate = [NSPredicate predicateWithFormat:@"SELF MATCHES %@", ipRegex];
	if (![ipPredicate evaluateWithObject:ipString])
	{
		UIAlertView *alertView = [[[UIAlertView alloc] initWithTitle:@"Invalid IP" message:@"Given IP address is invalid" delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil] autorelease];
		[alertView show];

		return;
	}


	// Validate port number
	NSString *portRegex = @"\\d{1,10}";
	NSPredicate *portPredicate = [NSPredicate predicateWithFormat:@"SELF MATCHES %@", portRegex];
	BOOL portIsValidNumber = [portPredicate evaluateWithObject:portString];
	uint16_t port = 0;
	if (portIsValidNumber)
		port = [portString intValue];
	if (!portIsValidNumber || port < 0 || port > 65535)
	{
		UIAlertView *alertView = [[[UIAlertView alloc] initWithTitle:@"Invalid Port" message:@"Port must be a positive integer between 0 and 65535 (inclusive)" delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil] autorelease];
		[alertView show];

		return;
	}

	// Now save settings and dismiss controller
	NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
	[defaults setObject:ipString forKey:userDefaultsIpAddressKey];
	[defaults setObject:[NSNumber numberWithUnsignedInt:port] forKey:userDefaultsPortNumberKey];

	[self dismissModalViewControllerAnimated:YES];
}

- (IBAction)cancelButtonTriggered:(id)sender
{
	[self dismissModalViewControllerAnimated:YES];
}


@end
