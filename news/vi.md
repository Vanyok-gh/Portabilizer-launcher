# Có gì mới trong Portabilizer

## v9.1

- Ngôn ngữ giao diện: tab «Ngôn ngữ» (có biểu tượng quả địa cầu), giống như trong cài đặt Windows: mỗi ngôn ngữ được hiển thị bằng tên riêng của nó, bên dưới là tên bằng ngôn ngữ giao diện. Cửa sổ, gợi ý, nhật ký, hộp thoại và lịch sử đều đã được dịch. Khi đổi ngôn ngữ, cửa sổ sẽ khởi động lại; cài đặt của bạn được giữ nguyên
- Ngôn ngữ: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Lần chạy đầu tiên sẽ dùng ngôn ngữ của Windows (nếu có trong số các ngôn ngữ đã dịch), nếu không thì dùng tiếng Anh
- Tệp portabilizer.log vẫn được ghi bằng tiếng Nga, giúp dễ xử lý lỗi hơn

## v9.0

- Không cần cài thư viện: chương trình tự nhận biết game hoặc ứng dụng cần thư viện nào và đề nghị đặt chúng cạnh exe (các tệp được tích hợp sẵn trong Portabilizer)
- DirectX: bản June 2010 và các bản cũ 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) cho game cũ
- Visual C++ 2010, 2012, 2013 và 2015-2022, OpenAL (cùng với wrap_oal.dll)
- Các bộ Cab mà chương trình không tự đọc được sẽ không còn bị bỏ qua: việc giải nén do expand.exe đảm nhận (Windows)
- Bộ thư viện được tạo bằng tập lệnh tools/collect_redist.bat

## v8.9

- Chế độ R: exe thông thường không còn được sao chép mà được chuyển vào thư mục App. Trên cùng một ổ đĩa việc này diễn ra tức thì và không cần thêm dung lượng (trước đây khi chạy cần gấp đôi dung lượng)
- Với tệp nén và trình cài đặt, Chế độ R vẫn cần dung lượng: chúng được giải nén trước, rồi mới xóa nguồn. Bạn có thể giải nén sang ổ đĩa khác bằng trường «Đích»
- Gợi ý và cửa sổ xác nhận của Chế độ R đã được cập nhật
- Biểu tượng bút pixel (xanh cho bản thông thường, đỏ cho R) với giao diện «Cổ điển (hệ thống)»; các giao diện khác giữ biểu tượng mượt

## v8.8

- Kiểm tra cập nhật: chương trình tự kiểm tra GitHub Releases và báo khi có phiên bản mới (có thể tắt bằng hộp kiểm trên tab «Phiên bản»)
- Hoạt động tốt hơn với Portabilizer Launcher: phiên bản dạng danh sách, mô tả «có gì mới», cài đặt chỉ một cú nhấp

## v8.7

- Giao diện: sáng, tối, giao diện đỏ cho Chế độ R, chọn màu của riêng bạn
- Tự động tìm 7-Zip đã cài
- Thư viện DirectX có sẵn trong chương trình (hiện hộp thoại nếu game thiếu chúng)
- Chạy không cần yêu cầu UAC cho các chương trình đòi quyền quản trị
- Đã xóa một gợi ý trùng lặp về bộ nhớ
