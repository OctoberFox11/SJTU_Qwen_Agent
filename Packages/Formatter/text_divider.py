class TextDivider:
    def __init__(self, threshold, overlap):
        self.threshold = threshold
        self.overlap = overlap

    @staticmethod
    def reverse(line_list):
        # 颠倒每个str_line中的str_character
        reversed_lines = [line[::-1] for line in line_list]
        # 颠倒每个line
        reversed_lines.reverse()
        return reversed_lines

    @staticmethod
    def headcutter(line_list, threshold, loose=True):
        current_chunk = []
        current_length = 0
        indices = []

        for i, line in enumerate(line_list):
            line_length = len(line)

            if loose:
                # 宽松分割逻辑
                if current_length + line_length > threshold:
                    indices.append(i)
                    current_chunk.append(line)
                    break
                else:
                    indices.append(i)
                    current_chunk.append(line)
                    current_length += line_length
            else:
                # 紧凑分割逻辑
                while line_length > 0:
                    if current_length + line_length > threshold:
                        remaining_length = threshold - current_length
                        if remaining_length > 0:
                            indices.append(i)
                            current_chunk.append(line[:remaining_length])
                            line = line[remaining_length:]
                            line_length -= remaining_length
                        return current_chunk, indices  # 达到阈值，返回当前块及其索引
                    else:
                        indices.append(i)
                        current_chunk.append(line)
                        current_length += line_length
                        break

        return current_chunk, indices

    def divide(self,txt_path):
        with open(txt_path, 'r', encoding='utf-8') as file:
            line_list = file.readlines()

        string_list = []
        loose_threshold = self.threshold
        tight_threshold = self.overlap
        # 使用 loose 模式获取第一个块及其索引
        current_chunk, current_chunk_indices = self.headcutter(line_list, loose_threshold, loose=True)
        line_list = [line for i, line in enumerate(line_list) if i not in current_chunk_indices]

        # 更新 loose_threshold 为 threshold - overlap
        loose_threshold = self.threshold - self.overlap
        string_list.append('\n'.join(current_chunk))
        while line_list:
            # 颠倒当前块
            reversed_chunk = self.reverse(current_chunk)

            # 使用 tight 模式获取重叠块及其索引
            overlap_chunk, overlap_chunk_indices = self.headcutter(reversed_chunk, tight_threshold, loose=False)

            # 颠倒重叠块以回正
            overlap_chunk = self.reverse(overlap_chunk)

            # 使用 loose 模式获取当前块并更新 line_list
            current_chunk, current_chunk_indices = self.headcutter(line_list, loose_threshold, loose=True)
            line_list = [line for i, line in enumerate(line_list) if i not in current_chunk_indices]

            # 把重叠块添加到当前块前面构成一个分割块
            current_chunk = overlap_chunk + current_chunk

            # 组合成字符串
            string_list.append('\n'.join(current_chunk))

        return string_list
