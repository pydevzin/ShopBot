from aiogram import Router, types
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile, InputMediaPhoto
from asgiref.sync import sync_to_async

from ..callback_data import CartImageCallbackData, RemoveCartItemCallbackData, MainMenuBackCallbackData
from ..keyboards.inline_button import cart_images_keyboard, cart_empty_keyboard
from ..sync_to_async_function import get_user_obj, get_cart_items, get_cart_items_simple
from ...shop.models import User, CartItem

router = Router()


@router.callback_query(F.data == "view_cart")
async def view_cart_handler(callback: types.CallbackQuery):
    user = callback.from_user
    user_obj = await get_user_obj(user.id)

    if not user_obj:
        return await callback.message.answer("Foydalanuvchi topilmadi.")  # noqa

    cart_items = await get_cart_items(user_obj)

    if not cart_items:
        return await callback.answer("🛒 Savatchangiz bo‘sh.", show_alert=True)  # noqa

    language = user_obj.language if user_obj else 'uz'

    current_item = cart_items[0]
    images = list(current_item.color_variant.images.all())

    if not images:
        return await callback.message.answer("Ushbu mahsulotning rasmi mavjud emas.")  # noqa

    image_path = images[0].image.path
    photo = FSInputFile(image_path)

    caption = (
        f"<b>{current_item.product.name_ru if language == 'ru' else current_item.product.name_uz}</b>\n"
        f"🎨 Rang: {current_item.color_variant.color_name}\n"
        f"💰 Narx: {current_item.color_variant.price} so'm"  # noqa
    )

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        parse_mode="HTML",
        reply_markup=await cart_images_keyboard(cart_items, 0, language)
    )


@router.callback_query(CartImageCallbackData.filter())
async def cart_image_pagination_handler(callback: types.CallbackQuery, callback_data: CartImageCallbackData):
    index = callback_data.index
    user = callback.from_user
    user_obj = await sync_to_async(User.objects.filter(telegram_id=user.id).first)()
    if not user_obj:
        return await callback.message.answer("Foydalanuvchi topilmadi.")  # noqa

    cart_items = await get_cart_items(user_obj)

    if not cart_items:
        return await callback.message.answer("Savatcha bo‘sh.")  # noqa

    if index < 0 or index >= len(cart_items):
        return await callback.answer("Bunday rasm yo‘q.")  # noqa

    item = cart_items[index]
    images = list(item.color_variant.images.all())

    if not images:
        return await callback.answer("Rasm topilmadi.")  # noqa

    photo = FSInputFile(images[0].image.path)
    language = user_obj.language if user_obj else 'uz'

    caption = (
        f"<b>{item.product.name_ru if language == 'ru' else item.product.name_uz}</b>\n"
        f"🎨 Rang: {item.color_variant.color_name}\n"
        f"💰 Narx: {item.color_variant.price} so'm"  # noqa
    )

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption,
            parse_mode="HTML"
        ),
        reply_markup=await cart_images_keyboard(cart_items, index, language)
    )


@router.callback_query(RemoveCartItemCallbackData.filter())
async def remove_cart_item_handler(callback: types.CallbackQuery, callback_data: RemoveCartItemCallbackData):
    user = callback.from_user
    item_id = callback_data.current_item_id

    user_obj = await sync_to_async(User.objects.filter(telegram_id=user.id).first)()
    if not user_obj:
        return await callback.answer("Foydalanuvchi topilmadi.")  # noqa

    cart_item = await sync_to_async(CartItem.objects.filter(id=item_id, user=user_obj).first)()
    if not cart_item:
        return await callback.answer("Mahsulot topilmadi yoki o‘chirilgan.")  # noqa

    await sync_to_async(cart_item.delete)()

    cart_items = await get_cart_items_simple(user_obj)

    await callback.message.delete()

    if not cart_items:
        return await callback.message.answer(
            "🛒 Savatchingiz bo‘sh.",  # noqa
            reply_markup=await cart_empty_keyboard(user_obj)
        )
    current_index = 0
    current_item = cart_items[current_index]
    language = user_obj.language

    caption = (
        f"<b>{current_item.product.name_uz if language == 'uz' else current_item.product.name_ru}</b>\n"
        f"🎨 Rang: {current_item.color_variant.color_name}\n"
        f"💰 Narx: {current_item.color_variant.price} so‘m"  # noqa
    )

    image_obj = await sync_to_async(current_item.color_variant.images.first)()
    if not image_obj:
        return await callback.message.answer("Rasm topilmadi.")  # noqa

    photo = FSInputFile(image_obj.image.path)

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        parse_mode="HTML",
        reply_markup=await cart_images_keyboard(cart_items, current_index, language)
    )

    await callback.answer("🗑️ Mahsulot o‘chirildi!")  # noqa
