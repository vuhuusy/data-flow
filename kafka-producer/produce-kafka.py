import csv
import time
from kafka import KafkaProducer

# Thiết lập Kafka Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092', 'localhost:9091'])

# Tên Kafka Topic
topic_name = 'vdt2024'

# Đường dẫn tới file CSV
csv_file_path = './log_action.csv'

def send_to_kafka(producer, topic, message):
    """
    Hàm để gửi message tới Kafka Topic
    """
    producer.send(topic, value=message.encode('utf-8'))
    producer.flush()

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

if __name__ == '__main__':
    read_csv_and_send_to_kafka(csv_file_path, producer, topic_name)
