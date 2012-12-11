//
//  UIImage+Extra.m
//  VMessenger
//
//  Created by User on 3/10/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "UIImage+Extra.h"
#import "DebugLog.h"

@implementation UIImage (Extra)

+ (UIImage *)safeImageNamed:(NSString *)name
{
    UIImage *image = [UIImage imageNamed:name];
    if (!image)
    {
        ALog(@"Image '%@' not found", name);
    }
    return image;
}

- (UIImage *)stretchableImage
{
	int width = self.size.width;
	int height = self.size.height;

	int capWidth = width / 2;
	if (0 == width % 2)
		--capWidth;

	int capHeight = height / 2;
	if (0 == height % 2)
		--capHeight;

	return [self resizableImageWithCapInsets:UIEdgeInsetsMake(capHeight, capWidth, capHeight, capWidth)];
}


@end
