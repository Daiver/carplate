//
//  UIImage+Extra.h
//  VMessenger
//
//  Created by User on 3/10/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface UIImage (Extra)

+ (UIImage *)safeImageNamed:(NSString *)name;

- (UIImage *)stretchableImage;

@end
