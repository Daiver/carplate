//
//  ViewController.m
//  CarPlateImageSender
//
//  Created by User on 12/9/12.
//  Copyright (c) 2012 Voronezh State University. All rights reserved.
//

#import "ViewController.h"

#import "ThirdParty/MBProgressHUD/MBProgressHUD.h"
#import "Utils/Utils.h"
#import "Globals.h"
#import "SettingsViewController.h"

typedef enum DataTag
{
	DataTagImageHeaderLength,
	DataTagImageHeader,
	DataTagImageData
} DataTag;

@interface ViewController ()

@property (assign, nonatomic) NSUInteger imageWidth;
@property (assign, nonatomic) NSUInteger imageHeight;
@property (assign, nonatomic) NSUInteger imageNumberOfChannels;

@end

@implementation ViewController
@synthesize imageView = _imageView;

- (void)dealloc
{
	[_imageView release];
	[super dealloc];
}

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
}

- (void)viewDidUnload
{
	[self setImageView:nil];
    [super viewDidUnload];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
	return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

- (IBAction)imageViewTouchUpInside:(id)sender
{
	UIImagePickerController *imagePicker = [[[UIImagePickerController alloc] init] autorelease];
	imagePicker.delegate = self;
	if ([UIImagePickerController isSourceTypeAvailable:UIImagePickerControllerSourceTypeCamera])
		imagePicker.sourceType = UIImagePickerControllerSourceTypeCamera;
	else
		imagePicker.sourceType = UIImagePickerControllerSourceTypePhotoLibrary;

	[self presentModalViewController:imagePicker animated:YES];
}

- (IBAction)settingsButtonTriggered:(id)sender
{
	SettingsViewController *settingsViewController = [[[SettingsViewController alloc] initWithNibName:@"SettingsViewController" bundle:nil] autorelease];
	[self presentModalViewController:settingsViewController animated:YES];
}

- (IBAction)sendButtonTriggered:(id)sender
{
	UIImage *image = self.imageView.image;
	if (!image)
		image = [UIImage safeImageNamed:@"carplate_transparent.png"];

	[MBProgressHUD showHUDAddedTo:self.view animated:YES];

	// Get image data
	CGImageRef imageRef = [image CGImage];
    NSUInteger width = CGImageGetWidth(imageRef);
    NSUInteger height = CGImageGetHeight(imageRef);
    NSUInteger bytesPerPixel = 4;
    NSUInteger bytesPerRow = bytesPerPixel * width;
    NSUInteger bitsPerComponent = 8;
	NSUInteger imageSizeBytes = height * bytesPerRow;
    CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB();
    uint8_t *rawData = (uint8_t *)malloc(imageSizeBytes);
    CGContextRef context = CGBitmapContextCreate(rawData, width, height,
												 bitsPerComponent, bytesPerRow, colorSpace,
												 kCGImageAlphaPremultipliedLast | kCGBitmapByteOrder32Big);
    CGColorSpaceRelease(colorSpace);

    CGContextDrawImage(context, CGRectMake(0, 0, width, height), imageRef);
    CGContextRelease(context);

	NSMutableString *imageString = [NSMutableString stringWithCapacity:imageSizeBytes * 5];
	for (NSUInteger i = 0; i < imageSizeBytes; ++i)
	{
		if ((i + 1) % 4 == 0)
			continue;
		[imageString appendFormat:@"%d, ", (int)rawData[i]];
	}

	free(rawData);
	NSData *imageData = [imageString dataUsingEncoding:NSUTF8StringEncoding];

	NSNumber *imageDataLengthNumber = [NSNumber numberWithUnsignedInteger:[imageData length]];
	NSNumber *widthNumber = [NSNumber numberWithUnsignedInteger:width];
	NSNumber *heightNumber = [NSNumber numberWithUnsignedInteger:height];
	NSNumber *channelsNumber = [NSNumber numberWithUnsignedInteger:3];

	NSDictionary *imageInfo = [NSDictionary dictionaryWithObjectsAndKeys:@[heightNumber, widthNumber, channelsNumber], @"shape", imageDataLengthNumber, @"size", nil];
	NSDictionary *requestData = [NSDictionary dictionaryWithObjectsAndKeys:imageInfo, @"args", @"recimage", @"method", nil];

	NSError *jsonConvertingError = nil;
	NSData *jsonData = [NSJSONSerialization dataWithJSONObject:requestData
													   options:kNilOptions
														 error:&jsonConvertingError];
	ZAssert(jsonConvertingError == nil, @"Failed to generate JSON data");



	GCDAsyncSocket *socket = [[[GCDAsyncSocket alloc] initWithDelegate:self delegateQueue:dispatch_get_main_queue()] autorelease];
	NSString *host = [[NSUserDefaults standardUserDefaults] objectForKey:userDefaultsIpAddressKey];
	NSNumber *portNumber = [[NSUserDefaults standardUserDefaults] objectForKey:userDefaultsPortNumberKey];
	if (!host || !portNumber)
	{
		[MBProgressHUD hideHUDForView:self.view animated:YES];

		NSString *title = @"Cannot connect";
		NSString *message;
		if (!host)
			message = @"IP address not specified";
		else
			message = @"Port number not specified";

		UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:title message:message delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
		[alertView show];
		return;
	}

	DLog(@"Connecting to %@:%@", host, portNumber);

	NSError *socketError = nil;
	if (![socket connectToHost:host
						onPort:[portNumber unsignedIntValue]
				   withTimeout:10
						 error:&socketError])
	{
		[MBProgressHUD hideHUDForView:self.view animated:YES];
		UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:@"Connection failed" message:@"Could not establish the connection" delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
		[alertView show];
		DLog(@"Connection failed: %@", socketError);
		return;
	}

	uint32_t jsonDataLength = htonl((uint32_t)[jsonData length]);
	[socket writeData:[NSData dataWithBytes:&jsonDataLength length:sizeof jsonDataLength] withTimeout:-1 tag:0];
	[socket writeData:jsonData withTimeout:-1 tag:0];
	[socket writeData:imageData withTimeout:-1 tag:0];

	[socket readDataToLength:sizeof(uint32_t) withTimeout:-1 tag:DataTagImageHeaderLength];
}


#pragma mark - GCDAsyncSocketDelegate

- (void)socket:(GCDAsyncSocket *)sock didReadData:(NSData *)data withTag:(long)tag
{
	switch (tag)
	{
		case DataTagImageHeaderLength:
		{
			uint32_t jsonLength = ntohl(*(uint32_t *)[data bytes]);
			[sock readDataToLength:jsonLength withTimeout:-1 tag:DataTagImageHeader];
			break;
		}
		case DataTagImageHeader:
		{
			NSError *jsonParseError = nil;
			NSDictionary *imageHeader = [NSJSONSerialization JSONObjectWithData:data
																		options:kNilOptions
																		  error:&jsonParseError];

			NSDictionary *imageData = [imageHeader objectForKey:@"args"];
			NSArray *imageShape = [imageData objectForKey:@"shape"];

			DLog(@"Image header:");
			DLog(@"%@", [[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding] autorelease]);

			ZAssert([imageShape count] == 3, @"Image shape must consist of 3 numbers");

			self.imageHeight = [[imageShape objectAtIndex:0] unsignedIntegerValue];
			self.imageWidth = [[imageShape objectAtIndex:1] unsignedIntegerValue];
			self.imageNumberOfChannels = [[imageShape objectAtIndex:2] unsignedIntegerValue];

			NSUInteger dataLength = [[imageData objectForKey:@"size"] unsignedIntegerValue];

			[sock readDataToLength:dataLength withTimeout:-1 tag:DataTagImageData];
			break;
		}
		case DataTagImageData:
		{
			DLog(@"Received data with length: %d", (int)[data length]);
			NSString *dataString = [[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding] autorelease];
			NSScanner *scanner = [NSScanner scannerWithString:dataString];
			[scanner setCharactersToBeSkipped:[[NSCharacterSet characterSetWithCharactersInString:@"0123456789"] invertedSet]];

			uint8_t *buffer = (uint8_t *)malloc(self.imageWidth * self.imageHeight * 4);
			uint8_t *pos = buffer;
			while (![scanner isAtEnd])
			{
				if ((pos - buffer + 1) % 4 == 0)
				{
					*pos++ = 255;
					continue;
				}
				int value;
				[scanner scanInt:&value];
				*pos++ = (uint8_t)value;
			}

			CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB();
			CGContextRef bitmapContext = CGBitmapContextCreate(buffer, self.imageWidth, self.imageHeight, 8, 4 * self.imageWidth, colorSpace,  kCGImageAlphaPremultipliedLast | kCGBitmapByteOrder32Big);
			CGImageRef cgImage = CGBitmapContextCreateImage(bitmapContext);

			UIImage *image = [UIImage imageWithCGImage:cgImage];

			CGContextRelease(bitmapContext);
			CGImageRelease(cgImage);
			CFRelease(colorSpace);
			free(buffer);

			DLog(@"image: %@", image);
			[self.imageView setImage:image];

			[MBProgressHUD hideHUDForView:self.view animated:YES];

			break;
		}
		default:
			break;
	}
}

- (void)socket:(GCDAsyncSocket *)sock didConnectToHost:(NSString *)host port:(uint16_t)port
{
	DLog(@"Successfully connected to host");
}

- (void)socketDidDisconnect:(GCDAsyncSocket *)sock withError:(NSError *)err
{
	DLog(@"Socket disconnected with error: %@", err);
	[MBProgressHUD hideHUDForView:self.view animated:YES];
	UIAlertView *alertView = [[[UIAlertView alloc] initWithTitle:@"Connection failed" message:[err localizedDescription] delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil] autorelease];
	[alertView show];
}


#pragma mark - UIImagePickerControllerDelegate

- (void)imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary *)info
{
	self.imageView.image = [info objectForKey:UIImagePickerControllerOriginalImage];

	[picker dismissModalViewControllerAnimated:YES];
}

@end
