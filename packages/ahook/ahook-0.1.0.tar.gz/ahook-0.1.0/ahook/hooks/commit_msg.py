#!/usr/bin/env python
# coding=utf-8

import os
import re

from hooklib import basehook as BaseHook, runhooks  # noqa: N812

from ahook.consts import W, R, G, B


CHARS_MAX_SIZE = 50


class ValidateCommitMessageHook(BaseHook):

    def check(self, log, rev_data):
        with open(rev_data.messagefile) as f:
            msg = f.read()
            msg_lines = [i for i in msg.splitlines() if not i.startswith('#')]

            # 写详情的话，摘要那行后，要有空行
            if len(msg_lines) >= 2 and msg_lines[1] != '':
                print_error_log(log)
                return False

            if len(msg_lines) >= 1:
                summary = msg_lines[0]

                # 中文得 decode 下才能计算正确的字符串 len
                if re_match(summary) and not [i for i in msg_lines if len(i.decode('UTF-8')) > CHARS_MAX_SIZE]:  # noqa: E501
                    return True

            print_error_log(log)
            return False


def print_error_log(log):
    log.write(os.linesep.join([
        'does not match like this:',
        R + '<type>(<scope>): <subject>',
        '# blank line',
        '<detail>' + W,
        '',
        'type 和 subject 必须，scope 可选',
        '',
        'type 有以下几种类型：',
        '  * feat - 新功能（feature）',
        '  * fix - 修补 bug',
        '  * docs - 文档（documentation）',
        '  * style - 格式（不影响代码运行的变动）',
        '  * refactor - 重构（即不是新增功能，也不是修改 bug 的代码变动）',
        '  * test - 增加测试',
        '  * chore - 构建过程或辅助工具的变动',
        '',
        'scope 用于说明 commit 影响的范围，比如：数据层、控制层、视图层等等，视项目不同而不同',  # noqa: E501
        '',
        'subject 是 commit 目的的简短描述，不超过 %d 个字符' % CHARS_MAX_SIZE,
        '',
        'eg:',
        G + 'feat(dashboard): init dashboard, ' + B + 'and NOT ENDSWITH DOT' + G,  # noqa: E501
        '',
        'Init dashboard app, and ' + B + 'MAX CHARS SIZE IS %d' % CHARS_MAX_SIZE + G,  # noqa: E501
        '- create pane',
        '- read pane',
        '- update pane',
        '- delete pane' + W,
    ]))


def re_match(summary):
    regex = re.compile(
        r'^(feat|fix|docs|style|refactor|test|chore)'  # type
        r'(\(.+\))?'  # (scope)
        r':( ){1}[^\s]{1}'  # 英文冒号后 1 个空格
        r'.*'  # 摘要内容
        r'(?<![\.|。|\s])$',  # 不能英文句号、中文句号、空格结尾
    )

    if re.match(regex, summary):
        return True
    else:
        return False


def main():
    runhooks('commit-msg', hooks=[ValidateCommitMessageHook])


if __name__ == '__main__':
    main()
