def bounding_box_coordinates(image_width, image_height, x_center, y_center, width, height):
    # To find the coord of the bounding boxes
    x_center_pixel = x_center * image_width
    y_center_pixel = y_center * image_height
    half_width = width * image_width / 2
    half_height = height * image_height / 2

    # To find the coord of the bounding boxes
    xmin = int(x_center_pixel - half_width)
    ymin = int(y_center_pixel - half_height)
    xmax = int(x_center_pixel + half_width)
    ymax = int(y_center_pixel + half_height)

    return xmin, ymin, xmax, ymax