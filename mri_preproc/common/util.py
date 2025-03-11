# Mixed bag of code I used for visualisation when experimenting
# with the code as a single script. Stashing it here as it could form
# the basis of a future QA report.

# import matplotlib.pyplot as plt
#
# def show_slices(slices):
#    """ Function to display row of image slices """
#    fig, axes = plt.subplots(1, len(slices))
#    for i, slice in enumerate(slices):
#        axes[i].imshow(slice.T, cmap="gray", origin="lower")
#
# #matplotlib.use('TkAgg')
# #matplotlib.use('qtcairo')
# slice_0 = img_data[50, :, :]
# slice_1 = img_data[:, 20, :]
# slice_2 = img_data[:, :, 20]
# show_slices([slice_0, slice_1, slice_2])
# plt.suptitle("Image slices")
# plt.savefig("/tmp/slices.pdf", format="pdf", bbox_inches="tight")
# # image data:
# # low z = bottom (i.e. image save feet to head)
# # low y = back (i.e. image back to front)
# # low z = right (of patient)
#
# ########
#
# ### Visualise the registration
# from dipy.viz import regtools
#
# transformed = affine_matrix.transform(moving_img)
#
# regtools.overlay_slices(
#     fixed_img,
#     transformed,
#     slice_index=None,
#     slice_type=0,
#     ltitle="Static",
#     rtitle="Transformed",
#     fname="/tmp/transformed_com_0.png",
# )
# regtools.overlay_slices(
#     fixed_img,
#     transformed,
#     slice_index=None,
#     slice_type=1,
#     ltitle="Static",
#     rtitle="Transformed",
#     fname="/tmp/transformed_com_1.png",
# )
# regtools.overlay_slices(
#     fixed_img,
#     transformed,
#     slice_index=None,
#     slice_type=2,
#     ltitle="Static",
#     rtitle="Transformed",
#     fname="/tmp/transformed_com_2.png",
# )
#
# # eog /tmp/transformed_com_*&
