(function() {
    'use strict';

    class SideMargin {
        constructor(largeSpaceWidth, spaceWidth) {
            this.largeSpaceWidth = largeSpaceWidth;
            this.spaceWidth = spaceWidth;
            this._largeSpaces = 0;
            this._spaces = 0;
            this.calculatedSize = 0;
        }
        recalculate() {
            this.calculatedSize = this.spaceWidth * this._spaces + this.largeSpaceWidth * this._largeSpaces;
        }
        clear() {
            this._largeSpaces = 0;
            this._spaces = 0;
            this.calculatedSize = 0;
        }
        moveSpacesAndLargeSpaces() {
            this._largeSpaces++;
            this._spaces = 0;
            this.recalculate();
        }
        setLargeSpaces(value) {
            this._largeSpaces = value;
            this.calculatedSize += this.largeSpaceWidth * value;
        }
        getLargeSpaces() {
            return this._largeSpaces;
        }
        setSpaces(value, recalculate) {
            this._spaces = value;
            if (recalculate) {
                this.recalculate();
                return;
            }
            this.calculatedSize += this.spaceWidth * value;
        }
        incrementSpaces() {
            this._spaces++;
            this.calculatedSize += this.spaceWidth;
        }
        getSpaces() {
            return this._spaces;
        }
        isPossibleToBuild(border) {
            //check if correct with space before text
            return !this._spaces || border || this._largeSpaces;
        }
        format(isLeft) {
            let res = '';
            let largeSpacesRemaining = this._largeSpaces;
            if (largeSpacesRemaining && (isLeft || largeSpacesRemaining > 1)) {
                res += tripleSpace;
                largeSpacesRemaining--;
            }
            if (this._spaces) {
                res += ' '.repeat(this._spaces);
            }
            if (largeSpacesRemaining > 0) {
                res += tripleSpace.repeat(largeSpacesRemaining);
            }
            return res;
        }
    }

    const tripleSpace = '⠀';

    $(document).ready(function(){
        const app = new Vue({
            el: '#app-formatter',
            delimiters: ['[[', ']]'],
            data: {
                input: '',
                output: '',
                roleLength: 165,
                invertDirection: false,
                mainMargin: false,
                secondMargin: false,
                customBorder: '',
                customBorderWidth: 0,
            },
            created() {
                const canvas = document.createElement("canvas");
                this.context = canvas.getContext("2d");
                this.context.font = '12px Whitney normal';

                this.largeSpaceWidth = this.context.measureText(tripleSpace).width;
                this.spaceWidth = this.context.measureText(' ').width;
                this.mainMargin = new SideMargin(this.largeSpaceWidth, this.spaceWidth);
                this.secondMargin = new SideMargin(this.largeSpaceWidth, this.spaceWidth);
                const wideRoleWidth = Math.trunc(this.context.measureText('WWWWWWWWWWWWWWWWWi').width);
                const narrowRoleWidth = Math.trunc(this.context.measureText('WWWWWWWWi').width);
                this.roleLengthOptions = [
                    [wideRoleWidth, `Wide - 1 row - ${wideRoleWidth}  pixels`],
                    [narrowRoleWidth, `Narrow - 1/2 of row - ${narrowRoleWidth}  pixels`],
                ];
                this.roleLength = wideRoleWidth;
            },
            watch: {
                input() {
                    this.recalculateIfPossible();
                },
                invertDirection() {
                    this.recalculateOutput();
                },
                roleLength() {
                    this.recalculateIfPossible();
                },
                customBorder(val) {
                    this.customBorderWidth = this.context.measureText(val).width;
                    this.recalculateIfPossible();
                }
            },
            methods: {
                recalculateIfPossible() {
                    if (!this.recalculateMargins()) {
                        // don't recalculate output if fail
                        return;
                    }
                    this.recalculateOutput();
                },
                copyResult(e) {
                    this.$refs.output.removeAttribute('disabled');
                    this.$refs.output.select();
                    document.execCommand("copy");
                    this.$refs.output.setAttribute('disabled', 'disabled');
                    $.notify({
                        message: e.target.getAttribute('data-success'),
                    }, {
                        type: 'success'
                    });
                },
                recalculateOutput() {
                    const leftMargin = this.invertDirection ? this.secondMargin : this.mainMargin;
                    const rightMargin = !this.invertDirection ? this.secondMargin : this.mainMargin;
                    this.output = this.customBorder + leftMargin.format(true) + this.input + rightMargin.format()
                        + this.customBorder;
                },
                getRoleNameWidth() {
                    // TODO: try to fix spaces between words
                    return this.context.measureText(this.input).width;
                },
                recalculateMargins() {
                    if (!this.input) {
                        return;
                    }

                    this.input = this.input.trim();

                    const emptySpace = this.roleLength - this.getRoleNameWidth() - this.customBorderWidth * 2;

                    if (emptySpace <= 0) {
                        $.notify({
                            message: 'Unable to format. Current Role length is greater than expected Role length.',
                        }, {
                            type: 'danger'
                        });
                        return;
                    }
                    // clear margins
                    this.mainMargin.clear();
                    this.secondMargin.clear();
                    if (emptySpace < this.spaceWidth) {
                        return true;
                    }
                    let mainSideEmptySpace = Math.ceil(emptySpace / 2);

                    this.mainMargin.setLargeSpaces(Math.trunc(mainSideEmptySpace / this.largeSpaceWidth));
                    mainSideEmptySpace -= this.mainMargin.calculatedSize;

                    this.mainMargin.setSpaces(Math.trunc(mainSideEmptySpace / this.spaceWidth));

                    let mainSideSingleSpacesSize = this.mainMargin.getSpaces() * this.spaceWidth;

                    let remainingEmptySpace = emptySpace - this.mainMargin.calculatedSize;

                    this.secondMargin.setLargeSpaces(Math.trunc(remainingEmptySpace / this.largeSpaceWidth));
                    remainingEmptySpace -= this.secondMargin.calculatedSize;
                    this.secondMargin.setSpaces(Math.trunc(remainingEmptySpace / this.spaceWidth));
                    remainingEmptySpace -= (this.secondMargin.getSpaces() * this.spaceWidth);

                    if (Math.trunc(
                        (this.mainMargin.getSpaces() * this.spaceWidth + remainingEmptySpace) / this.largeSpaceWidth
                    )) {
                        this.mainMargin.moveSpacesAndLargeSpaces();
                        remainingEmptySpace = emptySpace - this.secondMargin.calculatedSize - this.mainMargin.calculatedSize;
                    }

                    if (Math.trunc(remainingEmptySpace / this.spaceWidth)) {
                        this.mainMargin.incrementSpaces();
                        remainingEmptySpace -= this.spaceWidth;
                    }
                    // possible optimisations
                    // TODO: maybe delete this??
                    if (this.mainMargin.getLargeSpaces() === 1 && this.secondMargin.getSpaces() > 1) {
                        const possibleEmptySpace = (
                            (this.mainMargin.getSpaces() + this.secondMargin.getSpaces()) * this.spaceWidth
                            + remainingEmptySpace
                        );
                        if (possibleEmptySpace > this.largeSpaceWidth) {
                            this.mainMargin.moveSpacesAndLargeSpaces();
                            this.secondMargin.setSpaces(0, true);
                        }
                    }

                    // check for possibility of formatting
                    // TODO: maybe == 1
                    if (
                        !this.mainMargin.isPossibleToBuild(this.customBorder)
                        || !this.secondMargin.isPossibleToBuild(this.customBorder)
                    ) {
                        $.notify({
                            message: 'Unable to format this string ):',
                        }, {
                            type: 'danger'
                        });
                        return;
                        // TODO: clear result
                    }
                    // success
                    return true;
                }
            }
        });
    });
})();
