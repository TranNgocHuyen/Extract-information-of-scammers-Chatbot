import robot_img from "../assets/robot_image.png";
import { useState, useRef, useEffect } from "react";
import ScaleLoader from "react-spinners/ScaleLoader";
import { TypeAnimation } from "react-type-animation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMessage } from "@fortawesome/free-regular-svg-icons";

function ChatBot() {
  const messagesEndRef = useRef(null);
  const [timeOfRequest, setTimeOfRequest] = useState(0);
  const [promptInput, setPromptInput] = useState("");
  const [chatHistory, setChatHistory] = useState([
    {
      role: "assistant",
      content:
        "Chào anh, anh hỗ trợ thu hồi vốn treo phải không ạ? Anh tư vấn cho em với.",
    },
  ]);
  const [extractedInfo, setExtractedInfo] = useState("");

  const commonQuestions = [];
  const [isLoading, setIsLoading] = useState(false);
  const [isGen, setIsGen] = useState(false);
  const [dataChat, setDataChat] = useState([
    [
      "start",
      [
        "Chào anh, anh hỗ trợ thu hồi vốn treo phải không ạ? Anh tư vấn cho em với.",
        null,
      ],
    ],
  ]);

  useEffect(() => {
    scrollToEndChat();
  }, [isLoading]);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimeOfRequest((prevTime) => prevTime + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  function scrollToEndChat() {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  const onChangeHandler = (event) => {
    setPromptInput(event.target.value);
  };

  async function sendMessageChat() {
    if (promptInput !== "" && !isLoading) {
      setTimeOfRequest(0);
      setIsGen(true);
      setPromptInput("");
      setIsLoading(true);

      // Add user message to dataChat and chatHistory before sending API request
      setDataChat((prev) => [...prev, ["end", [promptInput, null]]]);
      setChatHistory((prev) => [
        ...prev,
        { role: "user", content: promptInput },
      ]);

      try {
        const response = await fetch(`http://localhost:8000/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "69420",
          },
          body: JSON.stringify({
            prompt: promptInput,
            history: chatHistory.map((msg) => ({
              role: msg.role,
              content: msg.content,
            })),
          }),
        });

        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();

        // If image_name exists, add the image to the chat
        if (result.image_name) {
          const imageUrl = `image/${result.image_name}`;
          setDataChat((prev) => [
            ...prev,
            ["start", [result.response.content, imageUrl]], // Include image URL
          ]);
        } else {
          setDataChat((prev) => [
            ...prev,
            ["start", [result.response.content, null]], // No image
          ]);
        }
        setChatHistory((prev) => [...prev, result.response]);

        // Fetch extracted information
        const extractedResponse = await fetch(`http://localhost:8000/data`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "69420",
          },
          body: JSON.stringify({
            history: [
              ...chatHistory,
              { role: "user", content: promptInput },
              result.response,
            ],
          }),
        });

        const extractedResult = await extractedResponse.json();
        const parsedObject = JSON.parse(extractedResult.data);
        setExtractedInfo(parsedObject);
      } catch (error) {
        console.error("Error during API request:", error);
        setDataChat((prev) => [
          ...prev,
          ["start", ["Lỗi, không thể kết nối với server", null]],
        ]);
      } finally {
        setIsLoading(false);
      }
    }
  }

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      sendMessageChat();
    }
  };

  function downloadXLSX() {
    // Convert the object into an array of arrays, each containing a key-value pair
    const data = Object.entries(extractedInfo).map(([key, value]) => [
      key,
      value,
    ]);

    // Extract keys for column headers
    const columns = data.map((item) => item[0]);

    // Extract values for the first row
    const values = data.map((item) => item[1]);

    // Create a new worksheet with columns as the first row and values as the second row
    const ws = XLSX.utils.aoa_to_sheet([columns, values]);

    // Create a new workbook
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Extracted Info");

    // Write the workbook to a binary string and create a download link
    XLSX.writeFile(wb, "extracted_info.xlsx");
  }

  return (
    <div className="bg-gradient-to-r from-blue-50 to-purple-100 h-[85vh]">
      <div className="hidden lg:block drawer-side absolute w-64 h-[20vh] left-3 mt-2 drop-shadow-md">
        <div className="menu p-4 w-full min-h-full bg-gray-50 text-base-content rounded-2xl mt-3 overflow-auto scroll-y-auto max-h-[80vh]">
          <ul className="menu text-sm">
            <h2 className="font-bold mb-2 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)]">
              Lịch sử trò chuyện
            </h2>
            {chatHistory.length === 0 ? (
              <p className="text-sm text-gray-500">
                Hiện chưa có cuộc hội thoại nào
              </p>
            ) : (
              chatHistory.map((mess, i) => (
                <li key={i}>
                  <p>
                    <FontAwesomeIcon icon={faMessage} />
                    {mess.content.length < 20
                      ? mess.content
                      : mess.content.slice(0, 20) + "..."}
                  </p>
                </li>
              ))
            )}
          </ul>
        </div>
      </div>
      <div className="hidden lg:block drawer-side absolute w-64 h-[20vh] mt-2 right-3 drop-shadow-md">
        <div className="menu p-4 w-full min-h-full bg-gray-50 text-base-content rounded-2xl mt-3 shadow-lg">
          <h2 className="font-bold text-lg mb-4 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text text-transparent">
            Thông tin trích xuất
          </h2>
          <div className="space-y-3">
            <div className="flex flex-col">
              <label className="font-semibold text-gray-600">Họ tên:</label>
              <p className="text-sm text-gray-800">
                {extractedInfo["Họ tên"] || "Chưa có thông tin"}
              </p>
            </div>
            <div className="flex flex-col">
              <label className="font-semibold text-gray-600">
                Số tài khoản:
              </label>
              <p className="text-sm text-gray-800">
                {extractedInfo["Số tài khoản"] || "Chưa có thông tin"}
              </p>
            </div>
            <div className="flex flex-col">
              <label className="font-semibold text-gray-600">Ngân hàng:</label>
              <p className="text-sm text-gray-800">
                {extractedInfo["Ngân hàng"] || "Chưa có thông tin"}
              </p>
            </div>
            <button
              onClick={downloadXLSX}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
              Tải xuống file excel
            </button>
          </div>
        </div>
      </div>
      <div className="flex justify-center h-[80vh]">
        <div
          id="chat-area"
          className="mt-5 text-sm scrollbar-thin scrollbar-thumb-gray-300 bg-white scrollbar-thumb-rounded-full scrollbar-track-rounded-full rounded-3xl border-2 md:w-[50%] md:p-3 p-1 w-full overflow-auto scroll-y-auto h-[80%]">
          {dataChat.map((dataMessages, i) =>
            dataMessages[0] === "start" ? (
              <>
                {/* Text Bubble */}
                <div
                  className="chat chat-start drop-shadow-md"
                  key={`text-${i}`}>
                  <div className="chat-image avatar">
                    <div className="w-10 rounded-full border-2 border-blue-500">
                      <img className="scale-150" src={robot_img} alt="Robot" />
                    </div>
                  </div>
                  <div className="chat-bubble chat-bubble-info break-words">
                    {/* Render text response */}
                    <TypeAnimation
                      style={{ whiteSpace: "pre-line" }}
                      sequence={[dataMessages[1][0], () => setIsGen(false)]}
                      cursor={false}
                      speed={100}
                    />
                  </div>
                </div>

                {/* Image Bubble */}
                {dataMessages[1][1] && (
                  <div
                    className="chat chat-start drop-shadow-md"
                    key={`image-${i}`}>
                    <div className="chat-image avatar">
                      <div className="w-10 rounded-full border-2 border-blue-500">
                        <img
                          className="scale-150"
                          src={robot_img}
                          alt="Robot"
                        />
                      </div>
                    </div>
                    <div className="chat-bubble chat-bubble-info">
                      <div className="mt-2">
                        <img
                          src={dataMessages[1][1]}
                          alt="Generated content"
                          className="rounded-lg max-w-full"
                        />
                      </div>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="chat chat-end" key={i}>
                <div className="chat-bubble shadow-xl chat-bubble-primary bg-gradient-to-r from-purple-500 to-blue-500 text-white">
                  {dataMessages[1][0]}
                </div>
              </div>
            )
          )}
          {isLoading && (
            <div className="chat chat-start">
              <div className="chat-image avatar">
                <div className="w-10 rounded-full border-2 border-blue-500">
                  <img src={robot_img} alt="Robot" />
                </div>
              </div>
              <div className="chat-bubble chat-bubble-info">
                <ScaleLoader
                  color="#000000"
                  loading={true}
                  height={10}
                  width={10}
                  aria-label="Loading Spinner"
                  data-testid="loader"
                />
                <p className="text-xs font-medium">{timeOfRequest + "/60s"}</p>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="absolute bottom-[0.2rem] left-1/2 transform -translate-x-1/2 md:w-[50%] w-[95%] grid">
        <input
          type="text"
          placeholder="Nhập câu hỏi tại đây..."
          className="shadow-xl border-2 focus:outline-none px-2 rounded-2xl input-primary col-start-1 md:col-end-12 col-end-11"
          onChange={onChangeHandler}
          onKeyDown={handleKeyDown}
          disabled={isGen}
          value={promptInput}
        />
        <button
          disabled={isGen}
          onClick={sendMessageChat}
          className="ml-1 drop-shadow-md md:col-start-12 rounded-2xl col-start-11 col-end-12 md:col-end-13 btn btn-active btn-primary btn-square bg-gradient-to-tl from-transparent via-blue-600 to-indigo-500">
          <svg
            stroke="currentColor"
            fill="none"
            strokeWidth="2"
            viewBox="0 0 24 24"
            color="white"
            height="15px"
            width="15px"
            xmlns="http://www.w3.org/2000/svg">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
        <p className="text-xs col-start-1 col-end-12 text-justify p-1">
          <b>Lưu ý: </b>Mô hình có thể trích xuất ra thông tin không chính xác ở
          một số trường hợp, vì vậy hãy luôn kiểm chứng thông tin bạn nhé!
        </p>
      </div>
    </div>
  );
}

export default ChatBot;
