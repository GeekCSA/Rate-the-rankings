import numpy as np
import torch
from sklearn.model_selection import train_test_split


class Data_Handler():
    def __init__(self, data_file_path, num_features):
        self.x = np.loadtxt(data_file_path, delimiter=',', usecols=range(num_features), skiprows=1)
        self.y = np.loadtxt(data_file_path, delimiter=',', usecols=[num_features], skiprows=1, dtype='str')

    def get_bulk(self):
        data = list(zip(self.x, self.y))
        np.random.shuffle(data)

        x = np.array([first for first, second in data])
        y = np.array([second for first, second in data])

        x_train, x_test, y_train, y_test = self.get_data_as_torch(x, y)

        return x_train, x_test, y_train, y_test

    def get_data_as_torch(self, x, y):

        x /= max(map(max, x))

        y = self.convert_chosen_str_to_num(y)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

        x_train = torch.from_numpy(x_train.astype(np.float32))
        x_test = torch.from_numpy(x_test.astype(np.float32))
        y_train = torch.from_numpy(y_train.astype(np.float32))
        y_test = torch.from_numpy(y_test.astype(np.float32))

        return x_train, x_test, y_train, y_test

    def convert_chosen_str_to_num(self, y):
        y = map(self.to_num, y)
        y = list(y)
        y = np.atleast_2d(y).T
        return y

    def to_num(self, chosen):
        if chosen == 'a':
            return 0
        elif chosen == 'b':
            return 1
        else:
            raise Exception("Chosen must be only 'a' or 'b'")


class Logistic_Reg_model(torch.nn.Module):
    def __init__(self, no_input_features):
        super(Logistic_Reg_model, self).__init__()
        self.layer1 = torch.nn.Linear(no_input_features, 1)
        # self.layer2 = torch.nn.Linear(8, 1)

    def forward(self, x):
        # y_predicted = self.layer1(x)
        y_predicted = torch.sigmoid(self.layer1(x))
        return y_predicted

def CrossEntropy(y_prediction, y_train):

    y_train = y_train.numpy()
    y_prediction = y_prediction.detach().numpy()

    total_loss = np.sum(-y_train * np.log(y_prediction) - (1 - y_train) * np.log(1 - y_prediction))
    num_samples = y_prediction.shape[0]
    mean_total = total_loss / num_samples

    return mean_total

def train_model(model, x_train, y_train, printable):
    lr = 0.1
    number_of_epochs = 100

    criterion = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(number_of_epochs):
        y_prediction = model(x_train)

        loss = criterion(y_prediction, y_train)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        if (epoch + 1) % 10 == 0 and printable:
            print('epoch:', epoch + 1, ',loss=', loss.item())


def test_model(model, x_test, y_test):
    with torch.no_grad():
        y_pred = model(x_test)
        y_pred_class = y_pred.round()
        accuracy = (y_pred_class.eq(y_test).sum()) / float(y_test.shape[0])
        print("Accuracy is: ", accuracy.item())

        return accuracy.item()


def main():
    data_file_path = 'Data/data.csv'
    num_features = 16

    super_data = Data_Handler(data_file_path, num_features)
    model = Logistic_Reg_model(num_features)

    num_epoch = 101
    sum_accuracy = 0
    for i in range(num_epoch):
        x_train, x_test, y_train, y_test = super_data.get_bulk()

        train_model(model, x_train, y_train, True)

        accuracy = test_model(model, x_test, y_test)
        sum_accuracy += accuracy

    print("\n\tAVG accuracy: ", str((sum_accuracy * 1.)/num_epoch))

    pass


if __name__ == '__main__':
    main()
