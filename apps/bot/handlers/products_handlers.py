from aiogram import Router, types
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.utils.i18n import gettext as _
from asgiref.sync import sync_to_async

from ..callback_data import ProductCallbackData, ProductImageCallbackData, AddToCartCallbackData
from ..keyboards.inline_button import product_images_keyboard
from ..sync_to_async_function import get_product_with_colors, get_user_obj, get_existing_item
from ...shop.models import ColorVariant, User, CartItem

router = Router()


@router.callback_query(ProductCallbackData.filter())
async def product_detail_callback_handler(callback: types.CallbackQuery,
                                          callback_data: ProductCallbackData,
                                          **data):
    user = data.get('user')
    language = user.language if user else 'uz'
    product_id = callback_data.product_id

    product = await get_product_with_colors(product_id)

    if not product:
        await callback.message.answer(_("Mahsulot topilmadi."))  # noqa
        return

    caption = f"<b>{product.name_ru if language == 'ru' else product.name_uz}</b>\n"

    first_image_path = None
    for color in product.colors.all():
        images = list(color.images.all())
        if images:
            first_image_path = images[0].image.path  # noqa
            break

    if not first_image_path:
        await callback.message.answer("Rasmlar mavjud emas.")  # noqa
        return

    photo = FSInputFile(first_image_path)

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        parse_mode="HTML",
        reply_markup=await product_images_keyboard(product, 0, language)
    )


@router.callback_query(ProductImageCallbackData.filter())
async def product_image_callback_handler(callback: types.CallbackQuery,
                                         callback_data: ProductImageCallbackData,
                                         **data):
    user = data.get("user")
    language = user.language if user else "uz"
    product_id = callback_data.product_id
    image_index = callback_data.image_index

    product = await get_product_with_colors(product_id)
    if not product:
        await callback.message.answer("Mahsulot topilmadi.")  # noqa
        return

    images_with_info = []
    for color in product.colors.all():
        for img in color.images.all():
            images_with_info.append({
                "image_path": img.image.path,
                "price": color.price,
                "color_name": color.color_name
            })

    if not images_with_info:
        await callback.message.answer("Rasmlar mavjud emas.")  # noqa
        return

    if image_index < 0 or image_index >= len(images_with_info):
        await callback.answer("Bunday rasm yo‘q.")  # noqa
        return

    image_info = images_with_info[image_index]  # noqa

    caption = f"<b>{product.name_ru if language == 'ru' else product.name_uz}</b>\n"
    caption += f"🎨 Rang: {image_info['color_name']}\n💰 Narx: {image_info['price']} so'm"  # noqa

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(image_info["image_path"]),
            caption=caption,
            parse_mode="HTML"
        ),
        reply_markup=await product_images_keyboard(product, image_index, language)
    )


@router.callback_query(AddToCartCallbackData.filter())
async def add_to_cart_handler(callback: types.CallbackQuery, callback_data: AddToCartCallbackData):
    user = callback.from_user
    color_variant_id = callback_data.color_variant_id

    user_obj = await get_user_obj(user.id)

    if not user_obj:
        return await callback.message.answer("Foydalanuvchi topilmadi.")  # noqa

    color_variant = await sync_to_async(ColorVariant.objects.select_related("product").filter)(id=color_variant_id)
    color_variant = await sync_to_async(color_variant.first)()

    if not color_variant:
        return await callback.message.answer("Mahsulot varianti topilmadi.")  # noqa

    existing_item = await get_existing_item(user_obj, color_variant)

    if not existing_item:
        await sync_to_async(CartItem.objects.create)(
            user=user_obj,
            product=color_variant.product,
            color_variant=color_variant
        )

    await callback.answer("🛒 Mahsulot savatchaga qo‘shildi!", show_alert=True)  # noqa
