//
//  ViewController.h
//  CarPlateImageSender
//
//  Created by User on 12/9/12.
//  Copyright (c) 2012 Voronezh State University. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ThirdParty/CocoaAsyncSocket/GCDAsyncSocket.h"

@interface ViewController : UIViewController <GCDAsyncSocketDelegate, UINavigationControllerDelegate, UIImagePickerControllerDelegate>

@property (retain, nonatomic) IBOutlet UIImageView *imageView;

@end
