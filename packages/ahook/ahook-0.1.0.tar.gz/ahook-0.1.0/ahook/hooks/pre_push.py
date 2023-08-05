#!/usr/bin/env python
# coding=utf-8

import os

from hooklib import basehook as BaseHook, runhooks  # noqa: N812

from ahook.consts import W, R, G


class DevelopGatingHook(BaseHook):

    # 示例：
    # feature/#9527
    # bugfix/#9527
    # hotfix/#9527
    # stable/1.1.x
    # develop
    # master
    # 其中 feature 由 feat fix docs style refactor test chore 的 commit 构成
    types = ('feature/', 'bugfix/', 'hotfix/', 'stable/', 'develop', 'master')

    def check(self, log, rev_data):
        has_check = False
        for rev in rev_data.revstobepushed:
            has_check = True
            if rev[0][len('refs/heads/'):].startswith(self.types):
                return True

        # 只有标记了，才执行 pre-push 错误提示
        if has_check:
            log.write(os.linesep.join([
                R + 'branch name invalid' + W,
                'should match like this:',
                G + 'feature/#9527',
                'bugfix/#9527',
                'hotfix/#9527',
                'stable/1.1.x',
                'develop',
                'master' + W,
            ]))

            return False

        return True


def main():
    runhooks('pre-push', hooks=[DevelopGatingHook])


if __name__ == '__main__':
    main()
