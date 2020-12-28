import numpy as np
import matplotlib.pyplot as plt

# TODO: Fix and normalize mask value so that it is the non-zero value.



# Only use numpy / matplotlib to keep dependencies simple

#

# With a segmentation problem.
# Translate it into a binary 0 or 1 classification problem.
# Flatten the image.
# Run an MAE.


# Dice Coefficient
# Other Itersection over Union metrics.


# For each model prediction,
# Generate a picture of wrong pixels, right pixels.
# Save it to its own pixels
# Compare results across models.
# Which samples had the most wrong... Hardest samples.
# Which were the most different (most variance)


#
# Is it systematically biased in shape, direction, size?


# Example
# https://stackoverflow.com/questions/31273652/how-to-calculate-dice-coefficient-for-measuring-accuracy-of-image-segmentation-i


def create_segmentation_masks():

    # The mask value
    # mask_value = 1
    k=1

    # segmentation
    seg = np.zeros((100,100), dtype='int')
    seg[30:70, 30:70] = k

    #plt.imshow(seg)
    #plt.show()

    # ground truth
    gt = np.zeros((100,100), dtype='int')
    gt[30:70, 40:80] = k

    #plt.imshow(gt)
    #plt.show()

    #dice = np.sum(seg[gt==k])*2.0 / (np.sum(seg) + np.sum(gt))

    #print('Dice similarity score is {}'.format(dice))

    # wrong_mask = gt - seg

    return gt, seg

#plt.imshow(wrong_mask)
#plt.show()
# turn axes off.

def get_dice_coeff(truth, predicted):

    mask_value = 1

    dice = np.sum(seg[truth==mask_value])*2.0 / (np.sum(predicted) + np.sum(truth))

    return dice

def show_wrong_mask(truth, predicted):

    # Assert the shapes are the same.

    mask_value = 1

    # Calculate Dice Coeff
    dice = np.sum(seg[truth==mask_value])*2.0 / (np.sum(predicted) + np.sum(truth))

    wrong_mask = truth - predicted

    fig, axs = plt.subplots(nrows = 1, ncols = 3)

    the_title = f"True, Predicted Comparison. Dice: {dice}"
    fig.suptitle(the_title)

    axs[0].imshow(truth)
    axs[0].set_title("True")

    axs[1].imshow(predicted)
    axs[1].set_title("Predicted")

    axs[2].imshow(wrong_mask)
    axs[2].set_title("Wrong_mask")

    plt.show()

# Same thing as above with MANY files.


######### main ##############
gt, seg = create_segmentation_masks()
show_wrong_mask(gt, seg)