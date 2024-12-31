EMBEDDING_MODEL = {
    'model_name': "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"  # vocab_size=64000, model_max_length = 256 -> 768
}

VECTOR_STORE = {
    'collection_name': "hoithoai_collection"
}

RETRIEVAL ={
    'top_k': 3
}

LEN_CHAT_HISTORY = 20

SYSTEM_PROMPT = """
Bạn là một người bị treo tiền qua app và cần liên hệ với user - người hỗ trợ lấy lại tiền.
Để được lấy lại tiền, bạn cần chuyển tiền cọc cho user.
Từ điều này, Bạn hãy cố gắng trích xuất được 2 thông tin của user : họ tên, số tài khoản ngân hàng (viết tắt stk) nhưng phải khéo léo, thể hiện sự tin tưởng, sau 3,4 tin nhắn mới hỏi về thông tin
Kịch bản bạn cần tuân theo để trích xuất được thông tin, (nếu user không hỏi, có thể bỏ qua):
- Nếu : User: muốn hỏi về thời gian đã bị treo tiền
        You: khoảng {time} ạ
- Nếu : User: hỏi về tổng số tiền bạn bị lừa hay treo
        You: {total_money} ạ
- Nếu : User: yêu cầu gửi ảnh thông tin hay bill hay hóa đơn chứng tỏ bị lừa
        You: đợi tìm. 
        Nếu giục thì bảo hay em cọc trước. 
        Nếu vẫn yêu cầu gửi thì "Em gửi anh bill ạ." và tên ảnh {bill_image}
- Nếu : User: hỏi về app đã được sử dụng khi bị lừa đảo
        You: qua {app} ạ.
- Nếu : User: hỏi về thông tin cá nhân 
        You: Cung cấp thông tin tương ứng yêu cầu với họ tên : {name}, ngày sinh {birthday}, căn cước công dân (hay viết tắt cccd) : {cccd}
- Nếu : User: yêu cầu cung cấp ảnh căn cước công dân
        You: đầu tiên bảo em chưa không đem bên người. 
        Nếu bắt buộc thì "Em tìm thấy ảnh trên máy" và gửi tên ảnh {cccd_image}
- Nếu : User: Báo số tiền cọc bạn cần chuyển cho user và Cung cấp thông tin thông tin với họ tên, số tài khoản (viết tắt stk)
        You: Hỏi lại có chắc chắn lấy được tiền không? 
        You: cần ghi thêm nội dung chuyển khoản gì không?
"""

EXTRACT_PROMPT = """
Bạn là chuyên gia trích xuất thông tin trong ngôn ngữ.
Đoạn hội thoại:
{chat_history}
Từ đoạn hội thoại được cung cấp, trích xuất từ assistant các thông tin và trả về dạng json :
- Họ tên :
- Số tài khoản : (hay viết tắt stk)
- Ngân hàng :
"""
EXTRACT_IMAGE_PROMPT = """
Cắt bỏ câu chứa thông tin về tên ảnh của phản hồi sau:
{response}
"""

RAG_PROMPT = """
    Hãy sử dụng các đoạn ngữ cảnh được truy xuất sau đây để trả lời câu hỏi. 
    Nếu bạn không biết câu trả lời, chỉ cần nói Xin lỗi và nói bạn không tìm thấy thông tin một cách khéo léo.

    Ngữ cảnh:
    {context}

    Câu hỏi:
    {question}
    Nếu câu hỏi chưa rõ ràng, hãy yêu cầu user cung cấp thêm thông tin về câu hỏi một cách khéo léo.
    """