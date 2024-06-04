import csv
import time
from confluent_kafka import Producer

# Thiết lập Kafka Producer
conf = {
    'bootstrap.servers': 'localhost:9092,localhost:9091'
}
producer = Producer(**conf)

# Tên Kafka Topic
topic_name = 'vdt2024'

# Đường dẫn tới file CSV
csv_file_path = './log_action.csv'

def delivery_report(err, msg):
    """
    Callback khi nhận được phản hồi từ Kafka
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_to_kafka(producer, topic, message):
    """
    Hàm để gửi message tới Kafka Topic
    """
    producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
    producer.poll(0)

def read_csv_and_send_to_kafka(csv_file_path, producer, topic):
    """
    Hàm đọc dữ liệu từ file CSV và gửi từng message tới Kafka mỗi 1 giây
    """
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Bỏ qua header nếu có
        # next(csvreader)
        
        for row in csvreader:
            message = ','.join(row)
            send_to_kafka(producer, topic, message)
            print(f"Sent: {message}")
            time.sleep(1)
    
    # Wait for all messages to be delivered
    producer.flush()

if __name__ == '__main__':
    read_csv_and_send_to_kafka(csv_file_path, producer, topic_name)
